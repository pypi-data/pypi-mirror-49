import torch
import warnings
import matplotlib.pyplot as plt
import gc
import re
from torch import optim, nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from functools import partial

from legos.torch_utils import get_device, get_param_to_learn
from legos.datasets import DataBunch
from legos.events import (
    Events,
    SkipBackwardException,
    SkipBatchException,
    SkipEpochException,
    SkipOptimizerStepException,
    StopTrainException
)
from legos.callbacks import (
    ParamSchedulerCallback,
    OneCycleSchedulerCallback,
    get_common_callbacks
)
from legos.plugins import (
    get_default_plugins,
)
from legos.torch_utils import (
    to_device,
)

from legos.utils import (
    ifnone,
    get_temp_dir_path
)
from legos.forwarding import LEARNER_PLUGINS

class Learner():
    def __init__(self, model, data, optimizer, loss_func, callbacks=None, plugins=None, device=None, use_common_callbacks=False):
        self.device = device if device else get_device()
        self.model: nn.Module = model.to(self.device)
        self.opt: optim.Optimizer = optimizer
        self.loss_func = loss_func
        self.data: DataBunch = data
        self.callbacks = []
        if use_common_callbacks:
            callbacks = get_common_callbacks()
        self.add_cbs(callbacks)
        self.plugins = []
        if plugins is None:
            plugins = get_default_plugins()
        self.add_plugins(plugins)
        self.setup_plugins_forwarding(LEARNER_PLUGINS)
        self.training = False
        print("Device: ", next(self.model.parameters()).device)

    def add_cbs(self, cbs):
        if not cbs: return
        for cb in cbs:
            self.add_cb(cb)

    def add_cb(self, cb):
        if not cb: return
        cb.learner = self
        setattr(self, cb.name, cb)
        self.callbacks.append(cb)

    def remove_cb(self, cb):
        self.callbacks.remove(cb)
        delattr(self, cb.name)

    def add_plugins(self, plugins):
        if not plugins: return
        for plugin in plugins:
            self.add_plugin(plugin)

    def add_plugin(self, plugin):
        if not plugin: return
        plugin.learner = self
        setattr(self, plugin.name, plugin)
        self.plugins.append(plugin)

    def remove_plugin(self, plugin):
        self.plugins.remove(plugin)
        delattr(self, plugin.name)

    def setup_plugins_forwarding(self, config):
        for method_name, (plugin_name, target_method) in config.items():
            plugin = getattr(self, plugin_name, None)
            if plugin:
                plugin_method = getattr(plugin, target_method, None)
                if plugin_method:
                    setattr(self, method_name, plugin_method)
                else:
                    warnings.warn(f"{target_method} is not found in {plugin}")
            else:
                warnings.warn(f"{plugin_name} is not found in {self}")

    def cb(self, event: Events):
        for cb in self.sorted_callbacks:
            func = getattr(cb, event.value, None)
            if func is not None:
                func()

    def backward_pass(self, loss):
        try:
            self.cb(Events.BACKWARD_BEFORE)
            loss.backward()
            self.cb(Events.OPTIM_STEP_BEFORE)
            self.opt.step()
            self.opt.zero_grad()
            self.cb(Events.OPTIM_STEP_AFTER)
        except SkipBackwardException:
            self.cb(Events.SKIP_BACKWARD)
        except SkipOptimizerStepException:
            self.cb(Events.SKIP_OPTIMIZER_STEP)
        finally:
            self.cb(Events.BACKWARD_AFTER)

    def detach_tensor(self, tensor):
        if isinstance(tensor, (list, tuple)):
            tensor = list(map(lambda x: x.detach().cpu(), tensor))
        else:
            tensor = tensor.detach().cpu()
        return tensor

    def prepare_device(self, xb, yb, device=None):
        if not device:
            device = self.device
        if isinstance(xb, (list, tuple)):
            xb = list(map(partial(to_device, device), xb))
        else:
            xb = xb.to(device)

        if isinstance(yb, (list, tuple)):
            yb = list(map(partial(to_device, device), yb))
        else:
            yb = yb.to(device)
        return xb, yb

    def predict(self, xb):
        if isinstance(xb, (list, tuple)):
            pred = self.model(*xb)
        else:
            pred = self.model(xb)
        return pred

    def one_batch(self, xb, yb):
        try:
            self.cb(Events.BATCH_BEFORE)
            self.xb, self.yb = xb, yb

            xb, yb = self.prepare_device(xb, yb)
            pred = self.predict(xb)
            loss = self.loss_func(pred, yb)

            self.pred = self.detach_tensor(pred)
            self.loss = self.detach_tensor(loss)

            if self.training:
                self.backward_pass(loss)
        except SkipBatchException:
            self.cb(Events.SKIP_BATCH)
        finally:
            self.cb(Events.BATCH_AFTER)

    def one_epoch(self, dataloader):
        try:
            self.n_batches = len(dataloader)
            self.cur_dl = dataloader
            self.cb(Events.EPOCH_BEFORE)
            for self.batch_idx, (xb, yb) in enumerate(dataloader):
                self.one_batch(xb, yb)
        except SkipEpochException:
            self.cb(Events.SKIP_EPOCH)
        finally:
            self.cb(Events.EPOCH_AFTER)

    def fit(self, n_epochs=1):
        # TODO: Support resume at a specific batch_idx and epoch_idx
        try:
            self.n_epochs = n_epochs
            self.cb(Events.FIT_BEFORE)
            for self.epoch_idx in range(n_epochs):
                self.model.train()
                self.training = True
                self.one_epoch(self.data.train_dl)

                self.model.eval()
                self.training = False
                with torch.no_grad():
                    self.one_epoch(self.data.valid_dl)
        except StopTrainException:
            self.cb(Events.STOP_TRAIN)
        except KeyboardInterrupt:
            print("Keyboard Interrupt!")
        finally:
            self.cb(Events.FIT_AFTER)

    def fit_one_cycle(self, n_epochs, lr_max=0.003, start_pct=0.3,
                      div_factor=25, final_div_factor=None,
                      mom_max=0.95, mom_min=0.85):
        '''
        See `OneCycleSchedulerCallback`
        '''
        has_lr_scheduler = False
        for cb in self.sorted_callbacks:
            if isinstance(cb, ParamSchedulerCallback):
                params = cb.param_func_dict.keys()
                has_lr_scheduler = "lr" in params or "mom" in params
        if has_lr_scheduler:
            warnings.warn("This learner has already contained a parameter scheduler." +
                          "`fit_one_cycle`'s behaviour may be affected by these scheduler.")

        cb = OneCycleSchedulerCallback(lr_max=lr_max,
                                       div_factor=div_factor, final_div_factor=final_div_factor,
                                       start_pct=start_pct,
                                       mom_max=mom_max, mom_min=mom_min)
        self.add_cb(cb)
        self.fit(n_epochs)
        self.remove_cb(cb)

    def lr_find(self, max_iter=100, min_lr=1e-6, max_lr=10, plot_results=True, figsize=(20, 5)):
        '''
        Find the learning rate between `min_lr` and `max_lr` by
        changing the learning rate at every step and record the best loss.
        '''
        from legos.callbacks.lrfinder import LRFinderCallback
        from legos.callbacks.recorder import RecorderCallback
        from legos.callbacks.tqdm_cb import BatchTQDMCallback

        old_callbacks = self.callbacks
        tmp_path = get_temp_dir_path()/"tmp.pth"
        self.save(tmp_path, with_opt=True)

        self.callbacks = []

        lr_finder_cb = LRFinderCallback(max_iter, min_lr, max_lr)
        self.add_cb(lr_finder_cb)

        self.add_cb(BatchTQDMCallback(max_iter=max_iter))

        if plot_results:
            self.add_cb(RecorderCallback())

        self.fit(n_epochs=max_iter)

        lr_finder_cb.summary()

        if plot_results:
            _, axes = plt.subplots(nrows=1, ncols=2, figsize=figsize)
            self.recorder.plot_lr_loss(ax=axes[0])
            self.recorder.plot_lr(ax=axes[1])

        self.load(tmp_path, with_opt=True)
        self.callbacks = []
        self.add_cbs(old_callbacks)

    @property
    def sorted_callbacks(self):
        return sorted(self.callbacks, key=lambda cb: cb.order)

    @property
    def batch_info(self):
        state = 'Train' if self.training else 'Valid'
        return f'Epoch [{self.epoch_idx + 1:3d}/{self.n_epochs:3d}] Batch [{self.batch_idx + 1:4d}/{self.n_batches:4d}] - {state} -'

    @property
    def epoch_info(self):
        state = 'Train' if self.training else 'Valid'
        return f'Epoch [{self.epoch_idx + 1:3d}/{self.n_epochs:3d}] - {state} -'

    def get_lr(self, pg_id=-1):
        pg = self.opt.param_groups[pg_id]
        return pg.get('lr', None)

    def set_lr(self, lr, pg_id=-1):
        pg = self.opt.param_groups[pg_id]
        pg['lr'] = lr

    def get_model(self):
        return self.model

    def save(self, path, with_opt=True):
        if not hasattr(self, 'opt'): with_opt = False
        if with_opt:
            state = {'model': self.get_model().state_dict(), 'opt': self.opt.state_dict()}
        else:
            state = self.get_model().state_dict()
        torch.save(state, path)

    def load(self, path, with_opt=True, strict=True):
        state = torch.load(path, map_location=lambda storage, loc: storage)
        if set(state.keys()) == {'model', 'opt'}:
            model_state = state['model']
            self.get_model().load_state_dict(model_state, strict=strict)
            if with_opt and hasattr(self, 'opt'):
                self.opt.load_state_dict(state['opt'])
        else:
            if with_opt: warnings.warn("Saved file doesn't have optimizer state")
            self.get_model().load_state_dict(state, strict=strict)
        del state
        gc.collect()
        return self

    def learnable_parameters(self):
        return get_param_to_learn(self.model)

    def search_parameters(self, pattern, enable_grad, verbose=False):
        """
        Loop through each parameters and set the requires_grad until a pattern is matched in the parameter name.
        The pattern is matched using RegEx in the method `re.search`.
        Args:
        - pattern (string): a string to be matched using `re.search`
        - verbose (bool): print the results
        """
        for name, param in self.model.named_parameters():
            matched = re.search(pattern, name)
            if matched:
                if verbose:
                    print(f'Parameter: {name} - Matched = {matched} - Break')
                break
            param.requires_grad = enable_grad
            if verbose:
                print(f'Parameter: {name} - Matched = {matched} - requires_grad = {param.requires_grad}')

    def freeze_to(self, pattern, verbose=False):
        """
        Loop through each parameters and freeze until a pattern is matched in the parameter name.
        The pattern is matched using RegEx in the method `re.search`.
        Args:
        - pattern (string): a string to be matched using `re.search`
        - verbose (bool): print the results
        """
        self.search_parameters(pattern, enable_grad=False, verbose=verbose)

    def unfreeze_to(self, pattern, verbose=False):
        """
        Loop through each parameters and unfreeze until a pattern is matched in the parameter name.
        The pattern is matched using RegEx in the method `re.search`.
        Args:
        - pattern (string): a string to be matched using `re.search`
        - verbose (bool): print the results
        """
        self.search_parameters(pattern, enable_grad=True, verbose=verbose)

    def unfreeze_all(self):
        """
        Unfreeze all parameters
        """
        for param in self.model.parameters():
            param.requires_grad = True

class ClassLearner(Learner):

    def __init__(self, model, data, optimizer=None, loss_func=None, callbacks=None, device=None, add_hook_callbacks=False):
        optimizer = self.get_default_optimizer(model) if optimizer is None else optimizer
        loss_func = self.get_default_criterion() if loss_func is None else loss_func
        callbacks = self.get_default_callbacks() if callbacks is None else callbacks

        if add_hook_callbacks:
            from legos.callbacks import HookCallback, stats_hook, hists_hook
            hook_cb = HookCallback(True, False, forward_hook_funcs=[stats_hook, hists_hook], module_names=[])
            callbacks.append(hook_cb)

        super().__init__(model, data, optimizer, loss_func, callbacks=callbacks, device=device)

    def get_default_optimizer(self, model):
        return optim.Adam(model.parameters(), lr=0.1, betas=(0.9, 0.99))

    def get_default_criterion(self):
        return nn.CrossEntropyLoss()

    def get_default_callbacks(self):
        from legos.metrics import accuracy
        return get_common_callbacks(metrics=[accuracy])


class MaskLearner(Learner):
    """
    A Learner for learning masks which has the same resolution as the input. For example, image segmentation or denoising ...
    """

    def __init__(self, model, data, optimizer=None, loss_func=None, callbacks=None, device=None):

        optimizer = self.get_default_optimizer(model) if optimizer is None else optimizer
        loss_func = self.get_default_criterion() if loss_func is None else loss_func
        callbacks = self.get_default_callbacks() if callbacks is None else callbacks

        super().__init__(model, data, optimizer, loss_func, callbacks=callbacks, device=device)

    def get_default_optimizer(self, model):
        return optim.Adam(model.parameters(), lr=0.1, betas=(0.9, 0.99))

    def get_default_criterion(self):
        return nn.BCEWithLogitsLoss()

    def get_default_callbacks(self):
        return get_common_callbacks(metrics=self.get_default_metrics())

    def get_default_metrics(self):
        from legos.metrics import dice
        return [dice]

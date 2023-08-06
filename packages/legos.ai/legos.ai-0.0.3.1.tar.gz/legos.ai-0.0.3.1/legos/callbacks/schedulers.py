import torch
import math
import matplotlib.pyplot as plt
from functools import partial
from legos.callbacks import Callback
from legos.utils import ifnone

def sched_func(f):
    def _inner(start, end):
        return partial(f, start, end)
    return _inner

@sched_func
def linear_func(start, end, pos):
    return start + pos * (end - start)

@sched_func
def exp_func(start, end, pos):
    return start * (end / start) ** pos

@sched_func
def cos_func(start, end, pos):
    return start + (1 + math.cos(math.pi*(1-pos))) * (end-start) / 2

def combine_sched(percentages, list_funcs):
    assert sum(percentages) == 1
    assert len(percentages) == len(list_funcs)
    pcts = torch.tensor([0] + percentages)
    assert torch.all(pcts >= 0)
    pcts = torch.cumsum(pcts, 0)
    n_funcs = len(list_funcs)

    def combined(pos):
        sched_idx = (pos >= pcts).nonzero().max()
        sched_idx = min(sched_idx, n_funcs - 1)
        func = list_funcs[sched_idx]
        sched_pos = (pos - pcts[sched_idx]) / (pcts[sched_idx + 1] - pcts[sched_idx])
        return func(sched_pos)
    return combined

def plot_sched(f):
    outputs = [f(pos * 0.01) for pos in range(0, 100)]
    plt.plot(outputs)


class Scheduler():

    def __init__(self, step_func):
        self.step_func = step_func

    def step(self, batch_idx, epoch_idx, n_batches, n_epochs):
        total_iter = n_batches * n_epochs
        cur_iter   = n_batches * epoch_idx + batch_idx
        pos = cur_iter * 1.0 / total_iter
        self.step_func(pos)

class ParamSchedulerCallback(Callback):
    '''
    Schedule any hyperparameters that are registerd in optimizer param groups
    '''
    def __init__(self, param_func_dict, train_only=True):
        '''
        Args:
        param_func_dict (dict): a dictionary of parameter name and the function to schedule that parameter.
        train_only (bool): True if the parameter is updated only in training loop. False if one want to update in validation / testing. Default: True
        '''
        super().__init__()
        self.param_func_dict = param_func_dict
        self.train_only = train_only
        self.scheduler = Scheduler(self.update_param)

    def batch_before(self):
        if self.learner.training or not self.train_only:
            self.scheduler.step(
                batch_idx=self.learner.batch_idx,
                epoch_idx=self.learner.epoch_idx,
                n_batches=self.learner.n_batches,
                n_epochs=self.learner.n_epochs,)

    def update_param(self, pos):
        '''
        Update the parameter for each param groups in the Optimizer
        '''
        for name, func in self.param_func_dict.items():
            for pg in self.learner.opt.param_groups:
                if name in pg:
                    pg[name] = func(pos)

class OneCycleSchedulerCallback(ParamSchedulerCallback):
    '''
    Implementation of Leslie Smith’s 1cycle policy.
    See:
    - https://iconof.com/1cycle-learning-rate-policy/
    - https://docs.fast.ai/callbacks.one_cycle.html#What-is-1cycle?

    Steps:
    - Step 1: increase lr from `lr_max / div_factor` to `lr_max` using cosine function
                decrease mom from `mom_max` to `mom_min` using cosine function
    - Step 2: decrease lr from `lr_max` to `lr_max / final_div_factor` using cosine function
                increase mom from `mom_min` to `mom_max` using cosine function
    '''
    def __init__(self, lr_max, div_factor, final_div_factor, start_pct, mom_max, mom_min):

        assert 0. <= start_pct <= 1.0

        final_div_factor = ifnone(final_div_factor, div_factor * 1e4)

        lr_min = lr_max * 1.0 / div_factor
        lr_final = lr_max * 1.0 / final_div_factor

        self.lr_sched  = combine_sched([start_pct, 1.0 - start_pct],
                                       [cos_func(lr_min, lr_max), cos_func(lr_max, lr_final)])
        self.mom_sched = combine_sched([start_pct, 1.0 - start_pct],
                                       [cos_func(mom_max, mom_min), cos_func(mom_min, mom_max)])

        param_func_dict = {
            'lr': self.lr_sched,
            'momentum': self.mom_sched,
        }

        super().__init__(param_func_dict, True)

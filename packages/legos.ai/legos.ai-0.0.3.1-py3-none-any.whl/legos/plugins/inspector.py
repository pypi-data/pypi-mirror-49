import torch

from collections import OrderedDict
from beautifultable import BeautifulTable
from legos.plugins import Plugin
from legos.callbacks import HookCallback, SkipCallback, SkipValidationCallback
from legos.torch_utils import get_module_names
from legos.utils import get_temp_dir_path


def get_table():
    table = BeautifulTable()
    table.set_style(BeautifulTable.STYLE_SEPARATED)
    return table

def total_parameters(model, show_all=False):
    return sum(p.numel() for p in model.parameters() if p.requires_grad or show_all)

def show_parameters(model, show_all=False):
    headers = ["Parameter", "Size", "# elements"]
    if show_all:
        headers.append("Trainable")
    table = get_table()
    table.column_headers = headers

    for name, p in model.named_parameters():
        if p.requires_grad or show_all:
            row = [name, list(p.size()), p.numel()]
            if show_all:
                row.append(p.requires_grad)
            table.append_row(row)
    print(table)
    print("Total parameters: ", total_parameters(model, show_all))


class Inspector(Plugin):

    def summary(self, modules=True, parameters=True, profile=True, *args, **kwargs):
        """
        Call the summary_modules, show_parameters and profile in inspector plugin.
        This method uses *args and **kwargs to pass the extra parameters to each method.
        See each methods to know the exact paremeters.
        Args:
        - modules (bool): show the input and output size of each modules
        - parameters (bool): show the parameters size
        - profile (bool): do the profile and get the CPU and GPU time.
        """
        if modules:
            print("\n- summary_modules:")
            self.summary_modules(*args, **kwargs)
        if parameters:
            print("\n- show_parameters:")
            self.show_parameters(*args, **kwargs)
        if profile:
            print("\n- profile:")
            self.profile(*args, **kwargs)

    def total_parameters(self, show_all=False):
        return total_parameters(self.learner.model, show_all)

    def show_parameters(self, show_all=False, *args, **kwargs):
        return show_parameters(self.learner.model, show_all)

    def _activation_hook(self, hook, module, input, output):
        if isinstance(input, (list, tuple)):
            input_size = [list(i.shape) for i in input]
            if len(input_size) == 1:
                input_size = input_size[0]
        else:
            input_size = list(input.shape)

        if isinstance(output, (list, tuple)):
            output_size = [list(i.shape) for i in output]
            if len(output_size) == 1:
                output_size = output_size[0]
        else:
            output_size = list(output.shape)

        self.summary_results[hook.name]['input_size'] = input_size
        self.summary_results[hook.name]['output_size'] = output_size

    def summary_modules(self, train=False, *args, **kwargs):
        old_callbacks = self.learner.callbacks
        tmp_path = get_temp_dir_path() / "tmp.pth"
        self.learner.save(tmp_path, with_opt=True)

        self.learner.callbacks = []

        hook = HookCallback(True, False, forward_hook_funcs=[self._activation_hook], module_names=[])
        skip_batch = SkipCallback(batch_idx=0, verbose=False)
        skip_valid = SkipValidationCallback(verbose=False)
        self.learner.add_cbs([hook, skip_batch, skip_valid])

        self.summary_results = OrderedDict()
        names = get_module_names(self.learner.model)[1:]
        for name in names:
            self.summary_results[name] = dict()

        self.learner.fit(n_epochs=1)

        headers = ["Module", "Input Size", "Output Size"]
        table = get_table()
        table.column_headers = headers

        for name, result in self.summary_results.items():
            row = [name, result['input_size'], result['output_size']]
            table.append_row(row)

        print(table)

        self.learner.load(tmp_path, with_opt=True)
        self.learner.callbacks = []
        self.learner.add_cbs(old_callbacks)

    def profile(self, train=False, use_cuda=True, show_events=False, *args, **kwargs):
        cuda_available = torch.cuda.is_available()
        device = torch.device("cuda") if use_cuda and cuda_available else torch.device("cpu")

        xb, yb = self.learner.data.get_batch(train=train)
        xb, yb = self.learner.prepare_device(xb, yb, device=device)
        self.learner.model = self.learner.model.to(device)

        import torchprof
        with torchprof.Profile(self.learner.model, use_cuda=use_cuda) as prof:
            self.learner.predict(xb)
        self.learner.model.to(self.learner.device)

        print(prof.display(show_events=show_events))

    def show_graph(self, *args, **kwargs):
        import graphviz
        import warnings
        import hiddenlayer

        try:
            graphviz.version()
        except graphviz.ExecutableNotFound as e:
            warnings.warn("Check your GraphViz & hiddenlayer library installation. See: https://github.com/waleedka/hiddenlayer")
            raise e
        xb, yb = self.learner.data.get_batch()
        xb, yb = self.learner.prepare_device(xb, yb)
        graph = hiddenlayer.build_graph(self.learner.model, xb)
        return graph

    def memory(self, empty_cache=False):
        div_factor = 1024 * 1024
        print(f'Memory Allocated: {torch.cuda.memory_allocated() / div_factor :.3f} MB')
        print(f'Memory Cached:    {torch.cuda.memory_cached() / div_factor :.3f} MB')
        print(f'Max Memory Allocated: {torch.cuda.max_memory_allocated() / div_factor :.3f} MB')
        print(f'Max Memory Cached:    {torch.cuda.max_memory_cached() / div_factor :.3f} MB')

        if empty_cache:
            torch.cuda.empty_cache()
            print('\nAfter empty cache:')
            self.memory(empty_cache=False)

from torch import nn

class LayerActivation():
    features = None

    def __init__(self, m):
        self.hook = m.register_forward_hook(self.hook_fn)

    def hook_fn(self, m, inputs, outputs):
        self.features = outputs

    def __del__(self):
        self.remove()

    def remove(self):
        self.hook.remove()

from torch import nn

class Flatten(nn.Module):
    '''
    Flatten x to a 1d vector. Use at the end of the model
    '''
    def __init__(self, full=False):
        '''
        Args:
        - full: False if the first dimension is batch. True if the input is a rank-1 tensor. Default: False
        '''
        super().__init__()
        self.full = full

    def forward(self, x):
        return x.view(-1) if self.full else x.view(x.size(0), -1)
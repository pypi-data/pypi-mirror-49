from collections import OrderedDict
from torch import nn
from legos.layers import conv_layer, Flatten, adaptive_flatten
from legos.utils import ifnone

def simple_cnn(channels=[], kernel_sizes=None, strides=None, paddings=None, use_batch_norm=True, adaptive_func=nn.AdaptiveAvgPool2d):
    '''
    Create a simple conv model.

    Args:
    - channels: a list of channels of the model. The first value must be the input channels
    - kernel_sizes: a list of kernel sizes for each conv. If None, each conv kernel size will be 3
    - strides: a list of stride for each conv. If None, each conv stride will be 2
    '''
    n_layers = len(channels) - 1
    kernel_sizes = ifnone(kernel_sizes, [3] * n_layers)
    strides = ifnone(strides, [2] * n_layers)
    paddings = ifnone(paddings, [None] * n_layers)

    layers = [conv_layer(in_channels=channels[i],
                        out_channels=channels[i+1],
                        kernel_size=kernel_sizes[i],
                        stride=strides[i],
                        padding=paddings[i],
                        use_batch_norm=True if use_batch_norm and i < (n_layers - 1) else False,
                        use_relu=True if i < (n_layers - 1) else False
                        ) for i in range(n_layers)]
    layers.append(adaptive_flatten(adaptive_func, 1))
    return nn.Sequential(*layers)

def get_model_base(model:nn.Module, cut:int, freeze=False) -> nn.Module:
    layers = list(model.named_children())[:cut]
    model = nn.Sequential(OrderedDict(layers))
    if freeze:
        for param in model.parameters():
            param.requires_grad = False
    return model
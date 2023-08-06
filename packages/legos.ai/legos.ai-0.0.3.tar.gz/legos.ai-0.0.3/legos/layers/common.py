import torch
from torch import nn
from legos.utils import ifnone
from legos.layers.flatten import Flatten

def adaptive_flatten(adaptive_func, output_size):
    return nn.Sequential(adaptive_func(output_size), Flatten())

def relu(inplace:bool=False, leaky:float=None):
    return nn.LeakyReLU(inplace=inplace, negative_slope=leaky) if leaky else nn.ReLU(inplace=inplace)

def conv_layer(in_channels, out_channels, kernel_size, stride, padding=None, use_relu=True, use_batch_norm=True, leaky:float=None, is_1d=False):
    padding = ifnone(padding, kernel_size // 2)

    conv_func = nn.Conv1d if is_1d else nn.Conv2d
    conv = conv_func(in_channels=in_channels,
                     out_channels=out_channels,
                     kernel_size=kernel_size,
                     stride=stride,
                     padding=padding)

    layers = [conv]

    if use_relu: layers.append(relu(True, leaky))
    if use_batch_norm: layers.append(nn.BatchNorm2d(out_channels))

    return nn.Sequential(*layers)


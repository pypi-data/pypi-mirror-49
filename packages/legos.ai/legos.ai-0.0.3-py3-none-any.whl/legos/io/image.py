import numpy as np
import torch
import matplotlib.pyplot as plt
from legos.torch_utils import rgb_from_tensor

try:
    import skimage
    from skimage import io
except ModuleNotFoundError as e:
    print("Please install skimage at https://github.com/scikit-image/scikit-image")
    raise e

def open_image(path, expand_dims=False):
    img = io.imread(path)
    if len(img.shape) == 2 and expand_dims:
        img = np.expand_dims(img, axis=2)
    return img

def show_image(img, figsize=None, ax=None, alpha=None, axis=False, mean=None, std=None, to_float=False):
    if not ax:
        fig, ax = plt.subplots(figsize=figsize)
    if to_float:
        if type(img) is torch.Tensor:
            img = img.type(torch.float)
        if type(img) is np.ndarray:
            img = img.astype(np.float32)

    if type(img) is torch.Tensor:
        img = rgb_from_tensor(img, mean, std)

    ax.imshow(img, alpha=alpha)
    if not axis:
        ax.set_axis_off()
    return ax

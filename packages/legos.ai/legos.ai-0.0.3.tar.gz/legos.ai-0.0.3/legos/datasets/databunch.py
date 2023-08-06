import matplotlib.pyplot as plt
from torchvision.utils import make_grid
from legos.datasets.common import get_loaders
from legos.io import show_image
from legos.utils import ifnone

class DataBunch:
    def __init__(self, train_ds=None, valid_ds=None, batch_size=32):
        self.train_dl, self.valid_dl = get_loaders(train_ds, valid_ds, batch_size)

    def get_loader(self, train=True):
        dl = self.train_dl if train else self.valid_dl
        return dl

    def get_iterator(self, train=True):
        loader = self.get_loader(train=train)
        return iter(loader)

    def get_batch(self, train=True, iterator=None):
        if iterator is None:
            loader = self.get_loader(train=train)
            iterator = iter(loader)
        return next(iterator)

class ImageDataBunch(DataBunch):

    def plot_images(self, images, normalize=True, nrow=4, alpha=None, ax=None, figsize=(40, 20)):
        return show_image(make_grid(images, normalize=normalize, nrow=nrow), ax=ax, alpha=alpha, figsize=figsize)

    def show_batch(self, train=True, nrow=4, iterator=None):
        """
        Show a batch of images in grid
        Args:
        - train (bool): Use train loader of valid loader
        - nrow (integer): Number of images per row
        """
        iterator = ifnone(iterator, self.get_iterator(train))
        xs, ys = self.get_batch(train=train, iterator=iterator)
        return self.plot_images(xs, nrow=nrow), iterator

class ImageMaskDataBunch(ImageDataBunch):

    def show_batch(self, train=True, nrow=4, mask=True, iterator=None):
        """
        Show a batch of images in grid with mask
        Args:
        - train (bool): Use train loader of valid loader
        - nrow (integer): Number of images per row
        - mask (bool): Show the mask or not.
        """
        iterator = ifnone(iterator, self.get_iterator(train))
        xs, ys = self.get_batch(train=train, iterator=iterator)
        ax = self.plot_images(xs, nrow=nrow)
        if mask:
            ax = self.plot_images(ys, normalize=False, nrow=nrow, ax=ax, alpha=0.5)
        return ax, iterator
import torch
from pathlib import Path
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from torchvision.datasets import utils as tv_utils
from legos import TRAIN, VALID
from legos.datasets.transforms import get_transforms, TORCH_RGB_MEAN, TORCH_RGB_STD
from legos.datasets.common import get_loaders
from legos.utils import ifnone, extract_archive

def get_torchvision_dataset(dataset, root:str, download:bool=True, transform:transforms.Compose=None, *args, **kwargs):
    """
    Create training set and validation set from a PyTorch Dataset
    Args:
        dataset (torch.utils.data.Dataset): a PyTorch Dataset
        root (str): Root directory of dataset. Pass into `dataset`
        download (bool, optional): Pass into `dataset`
        transform (calllable, optional): Pass into `dataset`
    Returns:
        train_ds (torch.utils.data.Dataset): training set
        valid_ds (torch.utils.data.Dataset): validation set
    """
    train_ds = dataset(root=root, train=True, transform=transform[TRAIN], download=download, **kwargs)
    valid_ds = dataset(root=root, train=False, transform=transform[VALID], download=download, **kwargs)
    return train_ds, valid_ds

def get_mnist(download=True, root="../data"):
    transform = get_transforms(mean=(0.1307, ), std=(0.3081, ))

    return get_torchvision_dataset(datasets.MNIST,
                                   root=root,
                                   download=download,
                                   transform=transform)

def get_cifar_10(crop_size=224, random_flip=True, download=True,
                 root="../data", transform=None, mean=TORCH_RGB_MEAN, std=TORCH_RGB_STD):
    transform = ifnone(transform, get_transforms(mean, std, crop_size, random_flip))

    return get_torchvision_dataset(datasets.CIFAR10,
                                   root=root,
                                   download=download,
                                   transform=transform)

def get_hymenoptera(crop_size=224, random_flip=True, root="../data",
                    download=True, transform=None, mean=TORCH_RGB_MEAN, std=TORCH_RGB_STD):
    root = Path(root)
    img_folder = Path(root) / "hymenoptera_data"

    if download:
        tv_utils.download_url("https://download.pytorch.org/tutorial/hymenoptera_data.zip", root)
        extract_archive(str(root / "hymenoptera_data.zip"))

    data_transforms = ifnone(transform, get_transforms(mean, std, crop_size=crop_size, random_flip=random_flip))

    train_ds = datasets.ImageFolder(img_folder/'train', data_transforms[TRAIN])
    valid_ds = datasets.ImageFolder(img_folder/'val', data_transforms[VALID])

    return train_ds, valid_ds
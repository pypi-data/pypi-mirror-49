from legos import TRAIN, VALID
from legos.io import ls
from legos.datasets import ImageMaskDataset, ImageMaskDataBunch
from legos.datasets import get_segmentation_transforms
from legos.utils import to_path

def get_cavarna_dataset(train_img_dir, train_mask_dir, valid_img_dir=None, valid_mask_dir=None):
    train_source_list = [str(p) for p in to_path(train_img_dir).ls()]
    train_target_list = [str(p) for p in to_path(train_mask_dir).ls()]

    if valid_img_dir:
        valid_source_list = [str(p) for p in to_path(valid_img_dir).ls()]
    else:
        valid_source_list = []

    if valid_mask_dir:
        valid_target_list = [str(p) for p in to_path(valid_mask_dir).ls()]
    else:
        valid_target_list = []

    transform = get_segmentation_transforms()

    train_ds = ImageMaskDataset(train_source_list, train_target_list, transform=transform[TRAIN])
    valid_ds = ImageMaskDataset(valid_source_list, valid_target_list, transform=transform[VALID])

    return train_ds, valid_ds

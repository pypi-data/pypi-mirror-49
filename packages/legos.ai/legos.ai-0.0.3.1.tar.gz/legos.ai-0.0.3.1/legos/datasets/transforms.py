from torchvision import transforms
import albumentations as A
from albumentations.pytorch import ToTensor
from typing import Optional
from legos.constants import TRAIN, VALID

# Get from https://pytorch.org/docs/stable/torchvision/models.html#classification
TORCH_RGB_MEAN = [0.485, 0.456, 0.406]
TORCH_RGB_STD = [0.229, 0.224, 0.225]

def get_transforms(mean=TORCH_RGB_MEAN, std=TORCH_RGB_STD, crop_size: Optional[int]=None,
                   random_flip:bool = False,
                   shift_scale_rotate:bool = False):

    def compose(train):
        ops = []
        if train:
            if crop_size: ops.append(transforms.RandomResizedCrop(crop_size))
            if random_flip: ops.append(transforms.RandomHorizontalFlip())
        else:
            ops.append(transforms.CenterCrop(crop_size))
        ops.append(transforms.ToTensor())
        ops.append(transforms.Normalize(mean, std))
        return transforms.Compose(ops)

    data_transforms = {
        x: compose(x) for x in [TRAIN, VALID]
    }

    return data_transforms

def get_segmentation_transforms():
    train_transform = A.Compose([
        A.ShiftScaleRotate(),
        A.HorizontalFlip(),
        A.Normalize(TORCH_RGB_MEAN, TORCH_RGB_STD),
        ToTensor(),
    ])
    valid_transform = A.Compose([
        A.Normalize(TORCH_RGB_MEAN, TORCH_RGB_STD),
        ToTensor(),
    ])
    return {
        TRAIN: train_transform,
        VALID: valid_transform,
    }

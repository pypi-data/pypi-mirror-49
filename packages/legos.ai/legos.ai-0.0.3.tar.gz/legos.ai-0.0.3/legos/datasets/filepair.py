from torch.utils.data import Dataset
from legos.io import open_image

class FilePairDataset(Dataset):
    def __init__(self, source_list, target_list,
                 transform=None, target_transform=None):
        """
        Args:
        - source_list (list of str / Path): a list of source file paths
        - target_list (list of str / Path): a list of target file paths
        - transform: a transform that will be apply to source data
        - target_transform: a transform that will be apply to target data
        """
        if len(source_list) != len(target_list):
            raise "Source list and target list have different lengths"
        super().__init__()
        self.source_list, self.target_list = source_list, target_list
        self.transform, self.target_transform = transform, target_transform

    def __len__(self):
        return len(self.source_list)

    def open_file(self, path, is_source):
        raise NotImplementedError

    def apply_transforms(self, source, target):
        if self.transform is not None:
            source = self.transform(source)
        if self.target_transform is not None:
            target = self.target_transform(target)
        return source, target

    def __getitem__(self, index):
        source_path = self.source_list[index]
        target_path = self.target_list[index]
        source = self.open_file(source_path, True)
        target = self.open_file(target_path, False)
        return self.apply_transforms(source, target)


class ImagePairDataset(FilePairDataset):
    def __init__(self, source_list, target_list,
                 transform=None, target_transform=None, expand_dims=False):
        self.expand_dims = expand_dims
        super().__init__(source_list, target_list,
                         transform=transform, target_transform=target_transform)

    def open_file(self, path, is_source):
        return open_image(path, expand_dims=self.expand_dims)


class ImageMaskDataset(ImagePairDataset):

    def __init__(self, source_list, target_list, transform=None, expand_dims=False):
        """
        Note:
        - This Dataset uses albumentations transforms instead of torchvision transforms.

        Args:
        - transform: Should be transform from albumentations package which has parameters: image and mask.
        """
        return super().__init__(source_list, target_list, transform=transform,
                                target_transform=None, expand_dims=False)

    def apply_transforms(self, source, target):
        if self.transform is None:
            return source, target
        aug = self.transform(image=source, mask=target)
        return aug['image'], aug['mask']

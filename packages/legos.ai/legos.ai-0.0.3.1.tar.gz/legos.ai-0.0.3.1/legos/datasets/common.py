from torch.utils.data import (
    DataLoader,
    Subset,
    random_split,
)

def get_loaders(train_ds, valid_ds, batch_size, train_shuffle=True, valid_shuffle=False):
    train_dl = valid_dl = None
    if train_ds is not None:
        train_dl = DataLoader(train_ds, batch_size=batch_size, shuffle=train_shuffle)
    if valid_ds is not None:
        valid_dl = DataLoader(valid_ds, batch_size=batch_size, shuffle=valid_shuffle)
    return train_dl, valid_dl

def split_dataset(dataset, train_percent=0.8):
    if not (0 <= train_percent <= 1):
        raise ValueError("train_percent must be in range 0 to 1")
    train_len = int(train_percent * len(dataset))
    valid_len = len(dataset) - train_len

    return random_split(dataset, lengths=[train_len, valid_len])

def split_dataset_at_index(dataset, index):
    """
    Cut the dataset into half at the index position
    """
    if not (0 <= index <= len(dataset)):
        raise ValueError("Index position must be in the dataset length")
    indices = list(range(0, len(dataset)))
    return Subset(dataset, indices[0: index]), Subset(dataset, indices[index:])

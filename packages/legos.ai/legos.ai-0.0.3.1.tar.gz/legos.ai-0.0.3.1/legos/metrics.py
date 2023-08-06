import torch

def accuracy(pred, yb):
    '''
    Calculate accuracy for classification problem by:
    - Find the position of max value with argmax
    - Compare with the target values
    - Calculate the mean
    '''
    return (torch.argmax(pred, dim=1)==yb).detach().float().mean()

def dice(pred, labels):
    '''
    Dice coefficient metric.
    See:
        - https://en.wikipedia.org/wiki/S%C3%B8rensen%E2%80%93Dice_coefficient
        - https://inclass.kaggle.com/c/carvana-image-masking-challenge/overview/evaluation
    '''
    pred = (pred > 0).float()
    return 2. * (pred * labels).sum() / (pred + labels).sum()
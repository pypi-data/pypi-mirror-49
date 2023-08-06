import math
import torch
import matplotlib.pyplot as plt
import warnings
from legos.callbacks import Callback
from legos.torch_utils import exp_moving_average

class RunningStats():
    '''
    Calculate the metrics and save the running results as well as the raw results.
    '''

    def __init__(self, metrics=[], smooth_weight=0.5):
        assert 0. <= smooth_weight <= 1.
        if smooth_weight == 0. or smooth_weight == 1.:
            warnings.warn(f'smooth_weight ({smooth_weight}) may leads to non running stats.')
        self.metrics = metrics
        self.smooth_weight = torch.tensor(smooth_weight)
        self.reset()

    def __getitem__(self, key):
        '''
        Get the running results of `key`. If you need the raw results, use `.raw_stats[key]`.
        '''
        return self.running_stats[key].detach().cpu()

    def reset(self):
        self.raw_stats = {m.__name__: None for m in self.metrics}
        self.running_stats = {m.__name__: None for m in self.metrics}

    def calculate_mean(self, prev, cur, alpha):
        return exp_moving_average(prev, cur, alpha)

    def add(self, learner):
        with torch.no_grad():
            for metric in self.metrics:
                key = metric.__name__
                value = metric(learner.pred, learner.yb)
                self.raw_stats[key] = value

                if self.running_stats[key] is None:
                    self.running_stats[key] = value
                else:
                    running_value = self.calculate_mean(self.running_stats[key], value, self.smooth_weight)
                    self.running_stats[key] = running_value.detach().cpu()

class StatsCallback(Callback):
    '''
    Calculate a list of running metrics to be used in other callbacks such as logging or recorder.
    The `order` of this StatsCallback is default as 0. Depended callbacks should have larger `order`.
    '''

    def __init__(self, metrics=[], smooth_weight=0.5):
        '''
        Args:
        metrics (list): a list of callable methods with the signature (pred, yb)
        smooth_weight (float, Optional): smoothing weight used in calculating running metrics. Default: 0.5
        '''
        super().__init__()
        self.metrics = metrics
        self.train_stats, self.valid_stats = RunningStats(self.metrics, smooth_weight), RunningStats(self.metrics, smooth_weight)

    @property
    def current_stats(self):
        return self.train_stats if self.learner.training else self.valid_stats

    def fit_before(self):
        self.train_stats.reset()
        self.valid_stats.reset()

    def batch_after(self):
        self.current_stats.add(self.learner)
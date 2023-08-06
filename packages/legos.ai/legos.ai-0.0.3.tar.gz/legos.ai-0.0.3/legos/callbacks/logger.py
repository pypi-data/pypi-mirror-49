import time
from legos.callbacks import Callback


class LoggerCallback(Callback):
    """
    LoggerCallback will print the loss in `Learner` and metrics in `StatsCallback` into console.
    Therefore, the `order` should be larger than `StatsCallback`.
    """

    order = 10

    def __init__(self, metrics=[], log_time=True, n_prints_per_epoch=1):
        super().__init__()
        self.metrics = metrics
        self.log_time = log_time
        self.n_prints_per_epoch = n_prints_per_epoch

    def fit_before(self):
        if not self.log_time: return
        self.fit_t1 = time.time()

    def fit_after(self):
        if not self.log_time: return
        self.fit_t2 = time.time()
        elapsed_time = self.fit_t2 - self.fit_t1
        duration = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
        print(f"Total Time = {duration}")

    def epoch_before(self):
        if not self.log_time: return
        self.epoch_t1 = time.time()

    def epoch_after(self):
        if not self.log_time: return
        self.epoch_t2 = time.time()
        elapsed_time = self.epoch_t2 - self.epoch_t1
        duration = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
        print(f"{self.learner.epoch_info} Epoch Time = {duration}")

    def batch_after(self):
        batch_idx = self.learner.batch_idx
        n_batches = self.learner.n_batches
        step = n_batches // self.n_prints_per_epoch

        if batch_idx % step == 0 or batch_idx == n_batches - 1:
            loss = self.learner.loss.item()
            metrics = self.metrics_summary()
            lr = self.learner.get_lr()
            print(f"{self.learner.batch_info} Loss = {loss:.6f}{metrics} - LR = {lr:.8f}")

    def metrics_summary(self):
        outputs = ''
        for metric in self.metrics:
            key = metric.__name__
            outputs += f' - {key} = {self.learner.stats.current_stats[key]:.6f}'
        return outputs
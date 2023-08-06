from legos.utils import is_notebook
from legos.callbacks import Callback


class TQDMCallback(Callback):

    def fit_before(self):
        if is_notebook():
            from tqdm import tqdm_notebook as tqdm
        else:
            from tqdm import tqdm
        self.master_bar = tqdm(total=self.learner.n_epochs)
        self.child_bar = tqdm()

    def fit_after(self):
        self.master_bar.close()
        self.child_bar.close()

    def epoch_before(self):
        total = self.learner.n_batches
        self.child_bar.reset(total)

    def batch_after(self):
        self.child_bar.update(1)

    def epoch_after(self):
        if not self.learner.training: return
        self.master_bar.update(1)


class BatchTQDMCallback(Callback):
    def __init__(self, max_iter, train=True, valid=False, *args, **kwargs):
        self.max_iter = max_iter
        self.train = train
        self.valid = valid
        return super().__init__(*args, **kwargs)

    def fit_before(self):
        if is_notebook():
            from tqdm import tqdm_notebook as tqdm
        else:
            from tqdm import tqdm
        self.master_bar = tqdm(total=self.max_iter)

    def fit_after(self):
        self.master_bar.close()

    def batch_after(self):
        if self.learner.training and not self.train:
            return
        if not self.learner.training and not self.valid:
            return

        self.master_bar.update(1)
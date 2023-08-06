from legos.callbacks import Callback
from legos.events import SkipEpochException


class SkipCallback(Callback):

    def __init__(self, batch_idx, verbose=True):
        super().__init__()
        self.verbose = verbose
        self.batch_idx = batch_idx

    def batch_after(self):
        if self.learner.model.training:
            batch_idx = self.learner.batch_idx
            n_batches = self.learner.n_batches
            if batch_idx == self.batch_idx:
                if self.verbose:
                    print(f"SkipCallback: SkipEpoch at {batch_idx + 1}/{n_batches}")
                raise SkipEpochException()


class SkipValidationCallback(Callback):

    def __init__(self, verbose=True):
        super().__init__()
        self.verbose = verbose

    def epoch_before(self):
        if self.learner.training is False:
            if self.verbose:
                print(f"SkipValidation: Skip Epoch {self.learner.epoch_idx}")
            raise SkipEpochException()

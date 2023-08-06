from legos.callbacks import (
    StatsCallback,
    LoggerCallback,
    RecorderCallback,
    TQDMCallback,
)
from legos.utils import ifnone

def get_common_callbacks(metrics=None):
    metrics = ifnone(metrics, [])
    if not isinstance(metrics, list):
        metrics = [metrics]
    stats_cb = StatsCallback(metrics=metrics, smooth_weight=0.5)
    log_cb = LoggerCallback(metrics=metrics)
    recorder_cb = RecorderCallback(metrics=metrics)
    tqdm_cb = TQDMCallback()

    return [stats_cb, log_cb, recorder_cb, tqdm_cb]

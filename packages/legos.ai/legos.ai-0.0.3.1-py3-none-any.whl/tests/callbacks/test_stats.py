import torch
import numpy
import hypothesis.strategies as st
from hypothesis import given
from legos.callbacks.stats import (
    StatsCallback,
    RunningStats
)
from legos.torch_utils import running_mean, compare_near


def test_stats_reset_in_fit_before(mocker):
    stats = StatsCallback()
    mocker.patch.object(stats, 'train_stats')
    mocker.patch.object(stats, 'valid_stats')

    stats.fit_before()

    stats.train_stats.reset.assert_called_once()
    stats.valid_stats.reset.assert_called_once()

def test_stats_current_stats(mocker):
    stats = StatsCallback()
    mocker.patch.object(stats, 'learner')
    mocker.patch.object(stats, 'train_stats')
    mocker.patch.object(stats, 'valid_stats')

    stats.learner.training = True
    assert stats.current_stats == stats.train_stats

    stats.learner.training = False
    assert stats.current_stats == stats.valid_stats

def test_stats_current_stats_add_called_once(mocker):
    stats = StatsCallback()
    mocker.patch.object(stats, 'learner')
    mocker.patch.object(stats, 'train_stats')
    mocker.patch.object(stats, 'valid_stats')

    stats.learner.training = True
    stats.batch_after()
    stats.current_stats.add.assert_called_once()

    stats.learner.training = False
    stats.batch_after()
    stats.current_stats.add.assert_called_once()

def test_running_stats(mocker):
    metric_value = mocker.Mock()
    metric_value.return_value = 'metric_value'
    metric_value.detach.return_value.cpu.return_value = metric_value
    metric_name = mocker.Mock()
    metric_name.return_value = 'metric_name'

    second_value = mocker.Mock()
    second_value.return_value = 'second_value'

    metric = mocker.Mock()
    metric.__name__ = metric_name
    metric.return_value = metric_value

    running = RunningStats(metrics=[metric])
    assert running.metrics == [metric]
    assert running.raw_stats == {metric_name: None}
    assert running.running_stats == {metric_name: None}

    learner = mocker.Mock()
    learner.pred = 'pred'
    learner.yb = 'yb'

    # 1st add
    running.add(learner)
    assert running.raw_stats == {metric_name: metric_value}
    assert running.running_stats == {metric_name: metric_value}

    assert running[metric_name] == metric_value
    assert running[metric_name] == running.running_stats[metric_name]

    # 2st add
    metric.return_value = second_value
    mean_value = mocker.Mock()
    mean_value.return_value = 'mean_value'
    mean_value.detach.return_value.cpu.return_value = mean_value

    running.calculate_mean = mocker.Mock()
    running.calculate_mean.return_value = mean_value

    running.add(learner)
    assert running.raw_stats == {metric_name: second_value}
    assert running.running_stats == {metric_name: mean_value}
    assert running[metric_name] == running.running_stats[metric_name]

@given(st.floats(allow_nan=False, allow_infinity=False, width=64),
       st.floats(allow_nan=False, allow_infinity=False, width=64),
       st.floats(allow_nan=False, allow_infinity=False, width=64))
def test_running_stats_calculate_mean_auto(prev, cur, alpha):
    mean = running_mean([prev, cur], alpha)

    running = RunningStats()
    output = running.calculate_mean(torch.tensor(prev), torch.tensor(cur), torch.tensor(alpha))

    if not torch.isnan(output) and not torch.isnan(mean):
        compare_near(output, mean)

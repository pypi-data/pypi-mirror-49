from legos.callbacks import LoggerCallback

def test_logger_time(mocker, capfd):
    logger = LoggerCallback(log_time=True)
    mocker.patch.object(logger, 'learner')
    logger.learner.batch_idx = 0
    logger.learner.n_batches = 10
    logger.learner.loss.item.return_value = 0.1
    logger.learner.get_lr.return_value = 0.1
    mocked_print = mocker.patch('builtins.print')

    logger.fit_before()
    logger.epoch_before()
    logger.batch_after()
    mocked_print.assert_called_once()
    mocked_print.reset_mock()
    logger.epoch_after()
    mocked_print.assert_called_once()
    mocked_print.reset_mock()
    logger.fit_after()
    mocked_print.assert_called_once()

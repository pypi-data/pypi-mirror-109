from sklearn import metrics


def r2_score(y_true, y_pred, *, sample_weight=None, multioutput='uniform_average'):
    """ R^2 (coefficient of determination) regression score function.
    Parameters
    ----------
    y_true : array-like of shape (n_samples,) or (n_samples, n_outputs)
        Ground truth (correct) target values.

    y_pred : array-like of shape (n_samples,) or (n_samples, n_outputs)
        Estimated target values.

    sample_weight : array-like of shape (n_samples,), default=None
        Sample weights.

    multioutput : {'raw_values', 'uniform_average', 'variance_weighted'}, \
            array-like of shape (n_outputs,) or None, default='uniform_average'

    Returns
    -------
    z : float or ndarray of floats
    """
    return metrics.r2_score(y_true, y_pred, sample_weight, multioutput)


def mean_squared_error(y_true, y_pred, *, sample_weight=None, multioutput='uniform_average', squared=True):
    """ Mean squared error regression loss.

    Parameters
    ----------
    y_true : array-like of shape (n_samples,) or (n_samples, n_outputs)
        Ground truth (correct) target values.

    y_pred : array-like of shape (n_samples,) or (n_samples, n_outputs)
        Estimated target values.

    sample_weight : array-like of shape (n_samples,), default=None
        Sample weights.

    multioutput : {'raw_values', 'uniform_average'} or array-like of shape (n_outputs,), default='uniform_average'

    squared : bool, default=True
        If True returns MSE value, if False returns RMSE value.

    Returns
    -------
    loss : float or ndarray of floats
    """
    return metrics.mean_squared_error(y_true, y_pred, sample_weight, multioutput, squared)


def root_mean_squared_error(y_true, y_pred, *, sample_weight=None, multioutput='uniform_average'):
    """ Root mean squared error regression loss.

    Parameters
    ----------
    y_true : array-like of shape (n_samples,) or (n_samples, n_outputs)
        Ground truth (correct) target values.

    y_pred : array-like of shape (n_samples,) or (n_samples, n_outputs)
        Estimated target values.

    sample_weight : array-like of shape (n_samples,), default=None
        Sample weights.

    multioutput : {'raw_values', 'uniform_average'} or array-like of shape (n_outputs,), default='uniform_average'

    squared : bool, default=True
        If True returns MSE value, if False returns RMSE value.

    Returns
    -------
    loss : float or ndarray of floats
    """
    return metrics.mean_squared_error(y_true, y_pred, sample_weight, multioutput, squared=False)

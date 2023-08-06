from sklearn import metrics


def accuracy_score(y_true, y_pred, *, normalize=True, sample_weight=None):
    """ Accuracy classification score.

    Parameters
    ----------
    y_true : 1d array-like, or label indicator array / sparse matrix
        Ground truth (correct) labels.

    y_pred : 1d array-like, or label indicator array / sparse matrix
        Predicted labels, as returned by a classifier.

    normalize : bool, default=True

    sample_weight : array-like of shape (n_samples,), default=None
        Sample weights.

    Returns
    -------
    score : float
    """
    return metrics.accuracy_score(y_true, y_pred, normalize, sample_weight)


def roc_auc_score(y_true, y_score, *, average="macro", sample_weight=None, max_fpr=None, multi_class="raise", labels=None):
    """ Compute Area Under the Receiver Operating Characteristic Curve (ROC AUC) from prediction scores.

    Parameters
    ----------
    y_true : array-like of shape (n_samples,) or (n_samples, n_classes)
        True labels or binary label indicators.

    y_score : array-like of shape (n_samples,) or (n_samples, n_classes)
        Target scores.

    average : {'micro', 'macro', 'samples', 'weighted'} or None, default='macro'

    sample_weight : array-like of shape (n_samples,), default=None

    max_fpr : float > 0 and <= 1, default=None

    multi_class : {'raise', 'ovr', 'ovo'}, default='raise'

    labels : array-like of shape (n_classes,), default=None

    Returns
    -------
    auc : float
    """
    return metrics.roc_auc_score(y_true, y_score, average, sample_weight, max_fpr, multi_class, labels)


def log_loss(y_true, y_pred, *, eps=1e-15, normalize=True, sample_weight=None, labels=None):
    """ Log loss, aka logistic loss or cross-entropy loss.

        L_{\log}(y, p) = -(y \log (p) + (1 - y) \log (1 - p))

    Parameters
    ----------
    y_true : array-like or label indicator matrix

    y_pred : array-like of float, shape = (n_samples, n_classes) or (n_samples,)
        Predicted probabilities.

    eps : float, default=1e-15
        Log loss is undefined for p=0 or p=1, so probabilities are
        clipped to max(eps, min(1 - eps, p)).

    normalize : bool, default=True
        If true, return the mean loss per sample.

    sample_weight : array-like of shape (n_samples,), default=None
        Sample weights.

    labels : array-like, default=None

    Returns
    -------
    loss : float
    """
    return metrics.log_loss(y_true, y_pred, eps, normalize, sample_weight, labels)


def f1_score(y_true, y_pred, *, labels=None, pos_label=1, average='binary', sample_weight=None, zero_division='warn'):
    """ Compute the F1 score, also known as balanced F-score or F-measure.

        F1 = 2 * (precision * recall) / (precision + recall)

    Parameters
    ----------
    y_true : 1d array-like, or label indicator array / sparse matrix
        Ground truth (correct) target values.

    y_pred : 1d array-like, or label indicator array / sparse matrix
        Estimated targets as returned by a classifier.

    labels : array-like, default=None

    pos_label : str or int, default=1

    average : {'micro', 'macro', 'samples','weighted', 'binary'} or None, default='binary'

    sample_weight : array-like of shape (n_samples,), default=None
        Sample weights.

    zero_division : "warn", 0 or 1, default="warn"

    Returns
    -------
    f1_score : float or array of float, shape = [n_unique_labels]
        F1 score of the positive class in binary classification or weighted
        average of the F1 scores of each class for the multiclass task.
    """
    return metrics.f1_score(y_true, y_pred, labels, pos_label, average, sample_weight, zero_division)


def fbeta_score(y_true, y_pred, *, beta, labels=None, pos_label=1, average='binary', sample_weight=None, zero_division='warn'):
    """ Compute the F-beta score.

    The F-beta score is the weighted harmonic mean of precision and recall,
    reaching its optimal value at 1 and its worst value at 0.

    Parameters
    ----------
    y_true : 1d array-like, or label indicator array / sparse matrix
        Ground truth (correct) target values.

    y_pred : 1d array-like, or label indicator array / sparse matrix
        Estimated targets as returned by a classifier.

    beta : float
        Determines the weight of recall in the combined score.

    labels : array-like, default=None

    pos_label : str or int, default=1

    average : {'micro', 'macro', 'samples', 'weighted', 'binary'} or None, default='binary'

    sample_weight : array-like of shape (n_samples,), default=None
        Sample weights.

    zero_division : "warn", 0 or 1, default="warn"

    Returns
    -------
    fbeta_score : float (if average is not None) or array of float, shape = [n_unique_labels]
    """
    return metrics.fbeta_score(y_true, y_pred, beta, labels, pos_label, average, sample_weight, zero_division)


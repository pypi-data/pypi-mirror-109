# Magic metrics library

## Description

``magic_metrics`` is library with the most usefull metrics from ``sklearn.metrics`` library in one place

## Content of Library

### Classification Metrics
- [accuracy_score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.accuracy_score.html)
- [roc_auc_score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_auc_score.html)
- [log_loss](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.log_loss.html)
- [f1_score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html)
- [fbeta_score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.fbeta_score.html)
        
### Regression Metrics
- [r2_score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.r2_score.html)
- [mean_squared_error](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_squared_error.html)
- [root_mean_squared_error]((https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_squared_error.html))

## Requirements
Before using the library make sure that [sklearn](https://scikit-learn.org/stable/install.html)  is  installed.

## Installation
```
git clone https://github.com/mshmnv/magic_metrics
```
or
```
pip install magic_metrics
```

The library can then be imported with:

```python

import magic_metrics
```

## Usage

```python
# Accuracy

>>> import magic_metrics

>>> y_pred = [0, 2, 1, 3]
>>> y_true = [0, 1, 2, 3]
>>> magic_metrics.accuracy_score(y_true, y_pred)
0.5
```

```python
# ROC AUC

>>> from sklearn.datasets import load_breast_cancer
>>> from sklearn.linear_model import LogisticRegression
>>> import magic_metrics

>>> X, y = load_breast_cancer(return_X_y=True)
>>> clf = LogisticRegression(solver="liblinear", random_state=0).fit(X, y)
>>> magic_metrics.roc_auc_score(y, clf.predict_proba(X)[:, 1])
0.99...
>>> magic_metrics.roc_auc_score(y, clf.decision_function(X))
0.99...
```


```python
# MSE
>>> y_true = [3, -0.5, 2, 7]
>>> y_pred = [2.5, 0.0, 2, 8]
>>> magic_metrics.mean_squared_error(y_true, y_pred)
0.375

>>> y_true = [3, -0.5, 2, 7]
>>> y_pred = [2.5, 0.0, 2, 8]
>>> magic_metrics.mean_squared_error(y_true, y_pred, squared=False)
0.612...
```

```python
# RMSE

>>> y_true = [3, -0.5, 2, 7]
>>> y_pred = [2.5, 0.0, 2, 8]
>>> magic_metrics.root_mean_squared_error(y_true, y_pred)
0.612...
```
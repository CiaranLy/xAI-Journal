"""Binary classification metrics without a scikit-learn dependency."""
import numpy as np
from scipy.stats import rankdata


def auc(y, p):
    """ROC AUC via the Mann-Whitney U statistic."""
    ranks = rankdata(p)
    n_pos = int(y.sum())
    n_neg = len(y) - n_pos
    return float((ranks[y == 1].sum() - n_pos * (n_pos + 1) / 2) / (n_pos * n_neg))


def binary_metrics(y, p, threshold=0.5):
    pred = (p >= threshold).astype(int)
    tp = int(((pred == 1) & (y == 1)).sum())
    tn = int(((pred == 0) & (y == 0)).sum())
    fp = int(((pred == 1) & (y == 0)).sum())
    fn = int(((pred == 0) & (y == 1)).sum())
    return {
        "accuracy": (tp + tn) / len(y),
        "sensitivity": tp / max(tp + fn, 1),
        "specificity": tn / max(tn + fp, 1),
        "auc": auc(y, p),
    }

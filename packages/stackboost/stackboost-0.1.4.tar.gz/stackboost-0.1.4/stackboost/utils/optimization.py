import numpy as np
from numba import jit
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans

@jit(nopython=True)
def min_max_sketch(X: np.ndarray, n_quantiles: int) -> np.ndarray:
    if len(np.unique(X)) > n_quantiles:
        delta = np.max(X) - np.min(X)
        quintile_size = delta / n_quantiles
        quintiles = np.array([quintile_size * (i + 1) for i in range(n_quantiles)])
    else:
        quintiles = np.unique(X)

    return quintiles


@jit(nopython=True)
def hist_sketch(X: np.ndarray, n_quantiles: int) -> np.ndarray:
    quintiles = np.histogram(a=X, bins=n_quantiles)[1]
    return quintiles


def cluster_sketch(X: np.ndarray, n_quantiles: int) -> np.ndarray:
    model = KMeans(n_clusters=n_quantiles)
    classes = model.fit_predict(X)
    clusters = [X[classes == i] for i in range(n_quantiles)]
    quintiles = np.array([(clusters[i].max() + clusters[i + 1].min()) / 2 for i in range(n_quantiles - 1)])
    return quintiles


def make_bins(X: np.ndarray, n_bins: int) -> np.ndarray:
    label_encoder =  LabelEncoder()
    n_columns = X.shape[1]
    for i in range(n_columns):
        X[:, i] = label_encoder.fit_transform(pd.cut(X[:, i], n_bins, retbins=True)[0])

    return X


def gradient_undersampling(gradients: np.ndarray, undersampling_percentage: float):
    flat_gradients = gradients.flatten()
    n_samples = flat_gradients.shape[0]
    absolute_gradients = np.abs(flat_gradients)
    indexes = absolute_gradients.argsort()[round(n_samples * undersampling_percentage):]
    mask = np.zeros(n_samples)
    mask[indexes] = 1
    return mask == 1

import numpy as np


def timeseries_to_connectome(path):
    """
    Estimate connectome from fMRI using the correlation matrix.
    """
    A = np.genfromtxt(path)
    G = np.corrcoef(A.T)
    return G

import numpy as np
import pandas as pd
from scipy import stats
from tqdm import tqdm

from ..utils import check_multigraphs


def _test(i, j, *multigraphs):
    """Calculate p-value for a specific edge."""

    # Subset samples by population
    samples = [subpop[:, i, j] for subpop in multigraphs]

    # A ValueError is thrown when the data columns passed to `stats.kruskal`
    # are equal. For example, stats.kruskal([0],[0]) throws such an error.
    try:
        _, pvalue = stats.kruskal(*samples)
        return pvalue
    except ValueError:
        return 1


def kruskal(*multigraphs):
    """
    Calculate the significance of edges between populations using the
    Krusal-Wallis Rank Sum test.

    Parameters
    ----------
    *multigraphs : list of multigraphs

    Returns
    -------
    pvals : pd.DataFrame
    """

    # Make iterator for traversing the upper triangle of the connectome
    multigraphs, n_vertices = check_multigraphs(*multigraphs)
    multigraphs = [np.array(multigraph) for multigraph in multigraphs]
    indices = zip(*np.triu_indices(n_vertices, 1))

    # Calculate p-values for each edge
    pvals = []
    for (i, j) in tqdm(indices):
        pvalue = _test(i, j, *multigraphs)
        pvals.append([i, j, pvalue])

    # Construct dataframe of results
    columns = ["i", "j", "p-value"]
    pvals = pd.DataFrame(pvals, columns=columns)

    return pvals

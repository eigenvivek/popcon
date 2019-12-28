import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from scipy import stats

from ..utils import check_multigraphs


def _test(i, j, *multigraphs):
    """Calculate p-value for a specific edge."""

    # Subset samples by population
    samples = [subpop[:, i, j] for subpop in multigraphs]

    # A ValueError is thrown when the data columns passed to `stats.kruskal`
    # are equal. For example, stats.kruskal([0],[0]) throws such an error.
    try:
        _, pvalue = stats.kruskal(*samples)
        return (i, j, pvalue)
    except ValueError:
        return (i, j, 1)


def kruskal(*multigraphs):
    """
    Calculate the significance of edges between populations using the
    Krusal-Wallis Rank Sum test.

    Parameters
    ----------
    *multigraphs : list of multigraphs
        Separate populations to be tested against each other

    Returns
    -------
    pvals : pd.DataFrame
        Dataframe of the p-value for each edge
    """

    # Make iterator for traversing the upper triangle of the connectome
    multigraphs, n_vertices = check_multigraphs(*multigraphs)
    multigraphs = [np.array(multigraph) for multigraph in multigraphs]
    indices = zip(*np.triu_indices(n_vertices, 1))

    # Calculate p-values for each edge
    pvals = Parallel(n_jobs=-1)(
        delayed(_test)(i, j, *multigraphs) for (i, j) in indices
    )

    # Construct dataframe of results
    columns = ["i", "j", "p-value"]
    pvals = pd.DataFrame(pvals, columns=columns)

    return pvals

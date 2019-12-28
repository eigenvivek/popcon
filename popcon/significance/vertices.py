import pandas as pd
from graspy.embed import OmnibusEmbed
from joblib import Parallel, delayed
from statsmodels.multivariate.manova import MANOVA

from ..utils import check_input_graphs


def _test(embedding, labels, vertex):
    """
    Test if embedding of a given vertex is significantly different across
    groups using MANOVA. The reported p-value is Pillai's trace.

    Parameters
    ----------
    embedding : np.ndarray, shape (n_samples, n_dim)
        Embedding of multigraph
    labels : np.array, shape (n_samples,)
        Class assignment for each graph
    vertex : int
        Which vertex in the embedding to test

    Returns
    -------
    vertex : int
        Input vertex
    pvalue : float
        P-value for the given vertex
    """
    vertex_embedding = embedding[:, vertex, :]
    sm = MANOVA(endog=vertex_embedding, exog=labels)
    pvalue = sm.mv_test().results["x0"]["stat"].values[1, 4]
    return (vertex, pvalue)


def manova(multigraph, labels):
    """
    Use MANOVA on graph embeddings to test if vertices are significantly
    different between different classes.

    Parameters
    ----------
    multigraph : Multigraph, shape (n_samples, n_vertices, n_vertices)
        A population of connectomes
    labels : array, shape (n_samples,)
        Class assignment for each graph

    Returns
    -------
    pvals : pd.DataFrame
        Dataframe containing p-value for each vertex
    """

    # Check the graphs
    multigraph, n_vertices = check_input_graphs(multigraph)

    # Embed each subpopulation
    omni = OmnibusEmbed()
    embedding = omni.fit_transform(multigraph)

    # Calculate p-values for each vertex
    pvals = Parallel(n_jobs=-1)(
        delayed(_test)(embedding, labels, vertex) for vertex in range(n_vertices)
    )

    # Construct dataframe of results
    columns = ["vertex", "p-value"]
    pvals = pd.DataFrame(pvals, columns=columns)

    return pvals

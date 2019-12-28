import pandas as pd
from graspy.embed import OmnibusEmbed
from joblib import Parallel, delayed
from statsmodels.multivariate.manova import MANOVA

from ..utils import check_input_graphs


def _test(embedding, labels, vertex, permutations):
    """
    Test if embedding of a vertex is significantly different across groups.

    P-value is Pillai's trace.
    """
    vertex_embedding = embedding[:, vertex, :]
    sm = MANOVA(endog=vertex_embedding, exog=labels)
    pvalue = sm.mv_test().results["x0"]["stat"].values[1, 0]
    return (vertex, pvalue)


def manova(multigraph, labels):

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

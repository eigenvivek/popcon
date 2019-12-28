from joblib import Parallel, delayed

import pandas as pd
from graspy.embed import OmnibusEmbed
from scipy.spatial.distance import pdist, squareform
from skbio.stats.distance import DistanceMatrix, permanova
from tqdm import tqdm

from ..utils import check_input_graphs


def _test(embedding, labels, vertex, permutations):
    """
    Test if embedding of a vertex is significantly different across groups.
    """

    # Construct dissimilarity matrix
    vertex_embedding = embedding[:, vertex, :]
    dissimilarity = DistanceMatrix(squareform(pdist(vertex_embedding)))

    # Calculate p-value
    result = permanova(dissimilarity, labels, permutations=permutations)
    return (vertex, result["p-value"])


def manova(multigraph, labels, permutations=1e4):

    # Check the graphs
    multigraph, n_vertices = check_input_graphs(multigraph)

    # Embed each subpopulation
    omni = OmnibusEmbed()
    embedding = omni.fit_transform(multigraph)

    # Calculate p-values for each vertex
    pvals = Parallel(n_jobs=-1)(
        delayed(_test)(embedding, labels, vertex, permutations)
        for vertex in range(n_vertices)
    )

    # Construct dataframe of results
    columns = ["vertex", "p-value"]
    pvals = pd.DataFrame(pvals, columns=columns)

    return pvals

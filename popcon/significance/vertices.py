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
    return result["p-value"]


def manova(multigraph, labels, permutations=1e4):

    # Check the graphs
    multigraph, n_vertices = check_input_graphs(multigraph)

    # Embed each subpopulation
    omni = OmnibusEmbed()
    embedding = omni.fit_transform(multigraph)

    # Calculate p-value for each vertex
    pvals = []
    for vertex in tqdm(range(n_vertices)):
        pvalue = _test(embedding, labels, vertex, int(permutations))
        pvals.append([vertex, pvalue])

    # Construct dataframe of results
    columns = ["vertex", "p-value"]
    pvals = pd.DataFrame(pvals, columns=columns)

    return pvals

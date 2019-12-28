import pytest
import numpy as np
from graspy.simulations import er_np

from popcon.significance import manova


def test_vertices():

    # Make a test multigraph
    pop_1 = [er_np(n=50, p=0.2) for _ in range(10)]
    pop_2 = [er_np(n=50, p=0.7) for _ in range(10)]
    graphs = pop_1 + pop_2
    graphs = np.array(graphs)
    labels = [0] * 10 + [1] * 10

    # Run the kruskal algorithm
    pvals = manova(graphs, labels)

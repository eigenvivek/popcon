import pytest
import numpy as np
from graspy.simulations import er_np

from popcon.significance import kruskal


def test_edges():

    # Make a test multigraph
    pop_1 = np.array([er_np(n=50, p=0.2) for _ in range(10)])
    pop_2 = np.array([er_np(n=50, p=0.7) for _ in range(10)])

    # Run the kruskal algorithm
    pvals = kruskal(pop_1, pop_2)

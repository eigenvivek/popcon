import pytest
from popcon.datasets import *


def test_mice():

    # Load the mouse dataset
    mice = load_mice()

    # Subset the BTBR genotype
    _, btbr = mice.multigraph.query("genotype == 'BTBR'")
    assert len(btbr) == 8

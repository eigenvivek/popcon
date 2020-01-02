import pytest

from popcon.datasets import load_mice


def test_mice():

    # Load the mouse dataset
    mice = load_mice()

    # Split population by genotype
    _, btbr = mice.multigraph.query("genotype == 'BTBR'")
    _, c57 = mice.multigraph.query("genotype == 'C57'")
    _, cast = mice.multigraph.query("genotype == 'CAST'")
    _, db2 = mice.multigraph.query("genotype == 'DB2'")

    assert mice.multigraph.df.shape == (32, 3)
    assert mice.blocks.shape == (14, 4)
    assert len(btbr) == len(c57) == len(cast) == len(db2) == 8

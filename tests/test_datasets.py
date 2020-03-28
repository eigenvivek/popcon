import pytest

from popcon.datasets import load_mice


def test_mice():

    # Load the mouse dataset
    mice = load_mice()

    # Split population by genotype
    _, btbr = mice.multigraph.query("genotype == 'BTBR'")
    _, b6 = mice.multigraph.query("genotype == 'B6'")
    _, cast = mice.multigraph.query("genotype == 'CAST'")
    _, dba2 = mice.multigraph.query("genotype == 'DBA2'")

    assert mice.multigraph.df.shape == (32, 3)
    assert mice.blocks.shape == (14, 4)
    assert len(btbr) == len(b6) == len(cast) == len(dba2) == 8

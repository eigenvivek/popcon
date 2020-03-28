import pytest

from popcon.datasets import load_mice
from popcon.significance import test_block


def test_sbm():

    mice = load_mice()

    _, btbr = mice.multigraph.query("genotype == 'BTBR'")
    _, b6 = mice.multigraph.query("genotype == 'B6'")
    _, cast = mice.multigraph.query("genotype == 'CAST'")
    _, dba2 = mice.multigraph.query("genotype == 'DBA2'")

    stat, pvalue = test_block(
        blocks=mice.blocks,
        expr_1="block=='isocortex' and hemisphere=='L'",
        expr_2="block=='pallium' and hemisphere=='L'",
        indep_test="Dcorr",
        samples=[btbr, b6, cast, dba2],
        mgc_kwargs={"reps": 10000, "workers": -1},
    )

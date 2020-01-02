import pytest

from popcon.datasets import load_mice
from popcon.significance import test_block


def test_sbm():

    mice = load_mice()

    _, btbr = mice.multigraph.query("genotype == 'BTBR'")
    _, c57 = mice.multigraph.query("genotype == 'C57'")
    _, cast = mice.multigraph.query("genotype == 'CAST'")
    _, db2 = mice.multigraph.query("genotype == 'DB2'")

    stat, pvalue = test_block(
        blocks=mice.blocks,
        expr_1="block=='isocortex' and hemisphere=='L'",
        expr_2="block=='pallium' and hemisphere=='L'",
        indep_test="Dcorr",
        samples=[btbr, c57, cast, db2],
        mgc_kwargs={"reps": int(1e5), "workers": -1},
    )

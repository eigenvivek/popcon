import pytest
from popcon.datasets import *


def test_mice():
    multigraph = load_mice()

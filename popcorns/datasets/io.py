from os.path import abspath, dirname, join

import numpy as np
import pandas as pd
from sklearn.utils import Bunch

from ..utils import Multigraph


def _get_datapath(path):
    """Get the absolute path to dataset."""
    root = abspath(dirname(__file__))
    return join(root, "data", path)


def _load_dataset(data_path):
    """Generage `Multigraph` object for a given dataset."""

    # Read the participant descriptor and graph tensor
    participants = pd.read_csv(join(data_path, "participants.csv"))
    graphs = np.load(join(data_path, "graphs.npy"))

    return Multigraph(participants, graphs)


def load_mice():
    """Load the Duke 2018 mouse data."""

    # Load the graphs
    data_path = _get_datapath(path="DUKE-BTBR")
    multigraph = _load_dataset(data_path)

    # Read the atlas
    atlas = pd.read_pickle(join(data_path, "atlas"))
    inner_hier_labels = atlas["Macrostructure"].tolist() * 2
    outer_hier_labels = np.array(166 * ["Right"] + 166 * ["Left"])

    return Bunch(
        multigraph=multigraph,
        structures=inner_hier_labels,
        hemisphere=outer_hier_labels,
    )

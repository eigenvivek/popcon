from os.path import abspath, dirname, join

import pandas as pd
from sklearn.utils import Bunch

from ..utils import Multigraph, load_edgelists, load_metrics, parse_participants


def _get_datapath(path):
    """Get the absolute path to dataset."""
    root = abspath(dirname(__file__))
    return join(root, "data", path)


def _load_dataset(data_path, extension):
    """
    Generage `Multigraph` object for a given dataset.

    Parameters
    ----------
    data_path : Path
        Path to BIDS-formatted dataset
    extension : string
        File extension for all edgelists in the dataset

    Returns
    -------
    Multigraph : Multigraph
        Multigraph object for the dataset
    """

    # Read the participant descriptor
    participants, param_dict = parse_participants(data_path)

    # Read the graphs
    sample_size = int(param_dict["sample_size"])
    n_vertices = int(param_dict["n_vertices"])
    graph_path = join(data_path, "graphs")
    graphs = load_edgelists(
        graph_path, participants, sample_size, n_vertices, extension
    )

    return Multigraph(participants, graphs)


def load_mice():
    """Load the Duke 2018 mouse data."""

    # Load the graphs
    data_path = _get_datapath(path="duke")
    multigraph = _load_dataset(data_path, extension="ssv")

    # Read metrics
    metrics_path = join(data_path, "metrics")
    metrics = load_metrics(metrics_path)

    # Read the atlas
    atlas = pd.read_csv(join(data_path, "atlas.csv"))

    # Read the sbm block structures
    blocks = pd.read_csv(join(data_path, "blocks.csv"))

    return Bunch(multigraph=multigraph, metrics=metrics, atlas=atlas, blocks=blocks,)

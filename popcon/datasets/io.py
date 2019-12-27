from itertools import takewhile
from os import listdir
from os.path import abspath, dirname, join

import networkx as nx
import numpy as np
import pandas as pd
from sklearn.utils import Bunch
from tqdm import tqdm

from ..utils import Multigraph


def _get_datapath(path):
    """Get the absolute path to dataset."""
    root = abspath(dirname(__file__))
    return join(root, "data", path)


def _parse_participants(data_path):

    participants_path = join(data_path, "participants.csv")

    # Get the dictionary of parameters
    param_dict = {}
    with open(participants_path, "r") as fobj:
        header_iter = takewhile(lambda s: s.startswith("#"), fobj)
        for item in header_iter:
            parameter, value = item[1:].split(":")
            parameter = parameter.strip()
            value = value.strip()
            param_dict[parameter] = value

    # Read the participants data
    participants = pd.read_csv(participants_path, comment="#")

    return participants, param_dict


def _load_edgelists(data_path, participants, sample_size, n_vertices, extension):

    # Make an empty tensor to hold the graphs
    graphs = np.zeros(shape=(sample_size, n_vertices, n_vertices))

    # Iterate over graphs and store them in `participants`
    for fl in tqdm(listdir(join(data_path))):

        if not fl.endswith(extension):
            continue

        subid = fl.split("_")[0]
        idx = participants.index[participants["participant_id"] == subid]

        with open(join(data_path, fl), "rb") as edgelist:
            G = nx.read_edgelist(edgelist)
            adj = nx.to_numpy_array(G, nodelist=sorted(G.nodes), dtype=np.float)
            graphs[idx[0]] = adj
            participants.at[idx, "slice"] = idx[0]

    return graphs


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
    participants, param_dict = _parse_participants("data_path")

    # Read the graphs
    sample_size = int(param_dict["sample_size"])
    n_vertices = int(param_dict["n_vertices"])
    graphs = _load_edgelists(
        data_path, participants, sample_size, n_vertices, extension
    )

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

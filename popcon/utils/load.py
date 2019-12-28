from itertools import takewhile
from os import listdir
from os.path import join

import networkx as nx
import numpy as np
import pandas as pd
from tqdm import tqdm


def parse_participants(data_path):

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


def load_edgelists(data_path, participants, sample_size, n_vertices, extension):

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

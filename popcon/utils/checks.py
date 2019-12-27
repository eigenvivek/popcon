from graspy.utils import import_graph
import numpy as np


def check_input_graphs(graphs):
    """
    Checks if all graphs in list have same shapes.

    Raises an ValueError if there are more than one shape in the input list,
    or if the list is empty or has one element.

    Parameters
    ----------
    graphs : list of nx.Graph or ndarray, or ndarray
        If list of nx.Graph, each Graph must contain same number of nodes.
        If list of ndarray, each array must have shape (n_vertices, n_vertices).
        If ndarray, then array must have shape (n_graphs, n_vertices, n_vertices).

    Returns
    -------
    out : ndarray, shape (n_graphs, n_vertices, n_vertices) 

    Raises
    ------
    ValueError
        If all graphs do not have same shape, or input list is empty or has 
        one element.
    """
    # Convert input to np.arrays
    # This check is needed because np.stack will always duplicate array in memory.
    if isinstance(graphs, (list, tuple)):
        if len(graphs) <= 1:
            msg = "Input {} must have at least 2 graphs, not {}.".format(
                type(graphs), len(graphs)
            )
            raise ValueError(msg)
        out = [import_graph(g, copy=False) for g in graphs]
    elif isinstance(graphs, np.ndarray):
        if graphs.ndim != 3:
            msg = "Input tensor must be 3-dimensional, not {}-dimensional.".format(
                graphs.ndim
            )
            raise ValueError(msg)
        elif graphs.shape[0] <= 1:
            msg = "Input tensor must have at least 2 elements, not {}.".format(
                graphs.shape[0]
            )
            raise ValueError(msg)
        out = import_graph(graphs, copy=False)
    else:
        msg = "Input must be a list or ndarray, not {}.".format(type(graphs))
        raise TypeError(msg)

    n_vertices = out[0].shape[0]
    return out, n_vertices


def check_multigraphs(*multigraphs):
    """
    Check that a set of multigraphs have the same shapes.
    """

    graphs = []
    vertex_sets = []

    for multigraph in multigraphs:
        out, n_vertices = check_input_graphs(multigraph)
        graphs.append(out)
        vertex_sets.append(n_vertices)

    if len(np.unique(vertex_sets)) != 1:
        msg = "Input graphs must have the same number of vertices."
        raise ValueError(msg)
    else:
        n_vertices = vertex_sets[0]

    return graphs, n_vertices

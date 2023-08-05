import numpy as np

from .utils import check_is_adj, check_compatible_adj


def graph_jaccard_index(g1, g2):
    """
    Compute the Graph Jaccard Index (GJI) between two graphs.

    Args:
        g1:
            np.ndarray
                Adjacency matrix of the first graph.
        g2:
            np.ndarray
                Adjacency matrix of the second graph.

    Returns:
        float
            Value of the GJI between the two graphs. The value will be in the
            [0, 1] range.

    References:
        Matteo Frigo, Emilio Cruciani, David Coudert, Rachid Deriche, Emanuele
        Natale, Samuel Deslauriers-Gauthier; Network alignment and similarity
        reveal atlas-based topological differences in structural connectomes.
        Network Neuroscience 2021; doi: https://doi.org/10.1162/netn_a_00199
    """
    check_is_adj(g1)
    check_is_adj(g2)
    check_compatible_adj(g1, g2)

    low = np.minimum(g1, g2)
    sum_min = low.ravel().sum()

    high = np.maximum(g1, g2)
    sum_max = high.ravel().sum()
    if sum_max == 0:
        sum_max = 1.

    return sum_min / sum_max

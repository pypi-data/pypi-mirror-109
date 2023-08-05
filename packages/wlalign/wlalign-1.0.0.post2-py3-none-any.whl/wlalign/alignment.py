import collections
import random
from typing import Optional

import numpy as np
from scipy.optimize import linear_sum_assignment

from .utils import check_is_adj, check_is_alignment, check_compatible_adj


def permutation_from_alignment(alignment: np.ndarray) -> np.ndarray:
    """
    Transform a matching into a permutation matrix.

    Args:
        alignment:
            np.ndarray
                n-by-2 array with one row per node in the graph. The node
                indexed by the first element of each row is mapped to the
                second element in each row

    Returns:
        np.ndarray
            Permutation matrix corresponding to the alignment
    """
    check_is_alignment(alignment)

    p = np.zeros([alignment.shape[0]] * 2)
    p[alignment.T[0], alignment.T[1]] = 1
    return p


def apply_alignment(graph: np.ndarray, alignment: np.ndarray) -> np.ndarray:
    """
    Permute the nodes of a graph according to a specified alignment.

    Args:
        graph:
            np.ndarray
                Graph that is being permuted.
        alignment:
            np.ndarray
                n-by-2 array with one row per node in the graph. The node
                indexed by the first element of each row is mapped to the
                second element in each row

    Returns:
        np.ndarray
            The permuted graph.
    """
    check_is_adj(graph)
    check_is_alignment(alignment)

    p = permutation_from_alignment(alignment)
    return p.transpose() @ graph @ p


def length_wl_signature(k: int, l: int) -> int:
    """
    Returns the length of the WL signature corresponding to the width and depth
    parameters given as input.

    Args:
        k:
            int
                Width of the breadth-first search.
        l:
            int
                Depth of the breadth-first search.

    Returns:
        int
            Length of the WL align signature.

    Raises:
        ValueError : if k <= 0.
        ValueError : if l <= 0.
    """
    if k <= 0:
        raise ValueError('Cannot have breadth-first search with negative '
                         'width.')
    if l <= 0:
        raise ValueError('Cannot have breadth-first search with negative '
                         'depth.')
    return sum([k ** i for i in range(l + 1)])


def signature_wl(g: np.ndarray, k: int, l: int, node: int,
                 volumes: Optional[list] = None) -> np.ndarray:
    """
    Compute the WL-align signature of a node of a graph from its adjacency
    matrix.

    Args:
        g:
            np.ndarray
                Adjacency matrix of the graph.
        k:
            int
                Width parameter of the breadth-first search.
        l:
            int
                Depth parameter of the breadth-first search
        node:
            int
                Index of the node of which the signature must be computed.
        volumes:
            Optional[list]
                List containing the volume of each node. If not passed, it's
                computed on the fly from the adjacency matrix.

    Returns:
        np.ndarray
            Signature of the node.

    References:
        Matteo Frigo, Emilio Cruciani, David Coudert, Rachid Deriche, Emanuele
        Natale, Samuel Deslauriers-Gauthier; Network alignment and similarity
        reveal atlas-based topological differences in structural connectomes.
        Network Neuroscience 2021; doi: https://doi.org/10.1162/netn_a_00199
    """
    check_is_adj(g)

    if volumes is None:
        volumes = np.sum(g, axis=1)
    elif len(volumes) != g.shape[0]:
        raise ValueError('The passed node volumes do not correspond to this '
                         'graph.')

    def f(path):
        if len(path) == 1:
            return volumes[path[0]]
        else:
            u = path[0]
            v = path[1]
            vv = volumes[u]
            if vv == 0:
                vv = 1
            return g[u, v] / vv * f(path[1:])

    n = g.shape[0]
    queue = collections.deque()
    queue.append([node])
    signature = np.zeros(length_wl_signature(k, l))
    idx = 0
    while queue:
        path = queue.popleft()
        signature[idx] = f(path)
        idx += 1
        if len(path) <= l:
            norms = []
            for z in range(n):
                path.append(z)
                # disconnected nodes have norm 0 and go at the end of the list
                # after sorting
                norms.append((z, f(path)))
                path.pop()
            random.shuffle(norms)  # ensures random tie breaks
            norms.sort(key=lambda x: -x[1])
            for z, fz in norms[:k]:
                queue.append(path + [z])

    return signature


def wl_align(g1: np.ndarray, g2: np.ndarray, k: int, l: int) -> np.ndarray:
    """
    Compute the WL alignment between two graphs as in Frigo et al., 2021.

    Args:
        g1:
            np.ndarray
                Adjacency matrix of the first graph to align.
        g2:
            np.ndarray
                Adjacency matrix of the second graph to align.
        k:
            int
                Width parameter of the breadth-first search.
        l:
            int
                Depth parameter of the breadth-first search

    Returns:
        np.ndarray
            Matrix with two columns and one row per node. The first element of
            each row is the index of the node in the first graph that is aligned
            with the node in the second graph indexed by the second element of
            the row.

    References:
        Matteo Frigo, Emilio Cruciani, David Coudert, Rachid Deriche, Emanuele
        Natale, Samuel Deslauriers-Gauthier; Network alignment and similarity
        reveal atlas-based topological differences in structural connectomes.
        Network Neuroscience 2021; doi: https://doi.org/10.1162/netn_a_00199
    """
    check_is_adj(g1)
    check_is_adj(g2)
    check_compatible_adj(g1, g2)

    volume1 = np.sum(g1, axis=1)
    volume2 = np.sum(g2, axis=1)

    n = g1.shape[0]
    signature1 = np.zeros((n, length_wl_signature(k, l)))
    signature2 = np.zeros_like(signature1)
    for u in range(n):
        signature1[u, :] = signature_wl(g1, k, l, u, volume1)
        signature2[u, :] = signature_wl(g2, k, l, u, volume2)

    c = np.zeros((n, n))
    for i, ui in enumerate(signature1):
        for j, vj in enumerate(signature2):
            c[i, j] = np.linalg.norm((ui - vj), 2)

    ind_row, ind_col = linear_sum_assignment(c)
    return np.array([ind_row, ind_col]).T

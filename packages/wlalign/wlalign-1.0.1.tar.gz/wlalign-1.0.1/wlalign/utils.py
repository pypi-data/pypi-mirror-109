import os
from typing import Optional

import numpy as np


def load_network(fpath: str, delimiter: str = ' ', skip: str = '#') -> \
        np.ndarray:
    """
    Load a network from a text file with the adjacency matrix

    Args:
        fpath:
            str
                Path of the file where the adjacency matrix is saved.
        delimiter:
            str
                Character that separates two consecutive entries in a row.
                Default: whitespace.
        skip:
            str
                Lines that start with this character will be skipped.

    Returns:
        np.ndarray
            The adjacency matrix.
    """
    g = np.loadtxt(fpath, comments=skip, delimiter=delimiter)
    check_is_adj(g)
    return g


def check_is_adj(g: np.ndarray):
    """
    Check if a matrix is an adjacency matrix

    Args:
        g:
            np.ndarray
                Matrix to be checked.

    Raises:
        ValueError : if the matrix is not 2-dimensional.
        ValueError : if the matrix is not square.
    """
    g = np.asanyarray(g)
    if g.ndim != 2:
        raise ValueError('The matrix is not 2-dimensional')
    if g.shape[0] != g.shape[1]:
        raise ValueError('The matrix is not square')


def check_is_alignment(alignment: np.ndarray, n: Optional[int] = None):
    """
    Check if a numpy array is a valid alignment.

    Args:
        alignment:
            np.ndarray
                Alignment to be checked. Must be n-by-2 numpy array.
        n :
            Optional[int]
                Number of nodes expected to be found in the alignment.

    Raises:
        ValueError : if the alignment does not have 2 dimensions.
        ValueError : if the alignment does not have 2 columns.
        ValueError : if the alignment does not have n rows.
        ValueError : if the alignment is not a 1-1 correspondence.
    """
    if alignment.ndim != 2:
        raise ValueError('The alignment must be 2-dimensional.')

    if alignment.shape[1] != 2:
        raise ValueError('The alignment must have 2 columns.')

    if n is not None and alignment.shape[0] != n:
        raise ValueError(f'The alignment must have {n} rows. '
                         f'Found: {alignment.shape[0]}.')

    if not np.array_equal(np.unique(alignment.T[0]), np.unique(alignment.T[1])):
        raise ValueError('The alignment is not a 1-1 correspondence.')


def check_can_write_file(fpath: str, force: bool = False) -> None:
    """
    Check if a file can be written.
    The function checks if the file already exists, the user has the permission
    to write it, overwriting can be forced and, if the file does not exist, if
    the parent directory exists and is writable.

    Args:
        fpath:
            str
                Path of the file to be checked.
        force:
            bool
                True if the file can be overwritten, False otherwise.

    Raises:
        FileExistsError : if the file exists and can not be overwritten.
        PermissionError :  if the file esists and the user does not have the
            permission to write it.
        PermissionError : if the file does not exist, the parent directory
            exists and the user does not have the permission to write a file in
            it.
        FileNotFoundError : if file does not exist and the parent directory
            does not exist.
    """
    if os.path.exists(fpath) and os.path.isfile(fpath):
        if os.access(fpath, os.W_OK):
            if force:
                return
            else:
                raise FileExistsError(f'Specify `--force` to overwrite '
                                      f'{fpath}')
        else:
            raise PermissionError(f'User does not have permission to write '
                                  f'{fpath}')
    else:
        d = os.path.dirname(os.path.abspath(fpath))
        if os.path.exists(d):
            if os.access(d, os.W_OK):
                return
            else:
                raise PermissionError(f'User does not have permission to '
                                      f'write file in directory {d}')
        else:
            raise FileNotFoundError(f'Directory does not exist: {d}')


def symmetrize_adj(g: np.ndarray) -> np.ndarray:
    """
    Transform a graph from directed to undirected by summing the weights in the
    two directions of each edge.

    Args:
        g:
            np.ndarray
                Adjacency matrix of the graph to symmetrize.

    Returns:
        np.ndarray
            Adjacency matrix of the symmetrized graph.
    """
    check_is_adj(g)
    return g + g.T - np.diag(np.diag(g))


def check_compatible_adj(g1: np.ndarray, g2: np.ndarray):
    """
    Check if two graphs have the same number of nodes.

    Args:
        g1:
            np.ndarray
                First graph to compare.
        g2:
            np.ndarray
                Second graph to compare.

    Raises:
        ValueError : if the two adjacency matrices do not have the same number
            of rows and columns.
    """
    check_is_adj(g1)
    check_is_adj(g2)

    if g1.shape != g2.shape:
        raise ValueError('The two graphs have different numbers of nodes.')

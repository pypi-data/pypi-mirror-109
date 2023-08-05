__version__ = '1.0.0.post2'

from . import alignment
from . import similarity
from . import utils

from .alignment import (apply_alignment, length_wl_signature,
                        permutation_from_alignment, signature_wl, wl_align)
from .similarity import graph_jaccard_index
from .utils import load_network, symmetrize_adj

gji = graph_jaccard_index  # alias for the graph Jaccard index

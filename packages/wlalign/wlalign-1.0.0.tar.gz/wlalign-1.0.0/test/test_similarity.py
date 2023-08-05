from unittest import TestCase

import numpy as np

from wlalign import similarity as wls


class TestJaccard(TestCase):
    def test_gji(self):
        g1 = np.array([[0, 1, 2],
                       [1, 0, 3],
                       [2, 3, 0]])
        g2 = np.array([[0, 1, 2],
                       [1, 0, 3],
                       [2, 3, 0]])

        np.testing.assert_almost_equal(wls.graph_jaccard_index(g1, g2), 1)

        g1 = np.array([[0, 1, 2],
                       [1, 0, 0],
                       [2, 0, 0]])
        g2 = np.array([[0, 0, 0],
                       [0, 0, 3],
                       [0, 3, 0]])

        np.testing.assert_almost_equal(wls.graph_jaccard_index(g1, g2), 0)

        g1 = np.array([[0, 1, 2],
                       [1, 0, 3],
                       [2, 3, 0]])
        g2 = np.array([[0, 1, 2],
                       [1, 0, 3 + 3],
                       [2, 3 + 3, 0]])

        np.testing.assert_almost_equal(wls.graph_jaccard_index(g1, g2), 12 / 18)

        g1 = np.zeros((3, 3))
        g2 = g1.copy()

        np.testing.assert_almost_equal(wls.graph_jaccard_index(g1, g2), 0)

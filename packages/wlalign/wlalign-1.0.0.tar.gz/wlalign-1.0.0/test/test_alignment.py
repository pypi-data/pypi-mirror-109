from unittest import TestCase

import numpy as np

from wlalign import alignment as wla


class TestAlignment(TestCase):
    def test_permutation_from_alignment(self):
        alignment = np.array([[0, 2],
                              [2, 1],
                              [1, 3],
                              [3, 0]])
        p = np.array([[0, 0, 1, 0],
                      [0, 0, 0, 1],
                      [0, 1, 0, 0],
                      [1, 0, 0, 0]])
        np.testing.assert_equal(p, wla.permutation_from_alignment(alignment))
        np.testing.assert_equal(np.abs(np.linalg.det(p)), 1)

    def test_apply_alignment(self):
        g = np.array([[0., 1., 2., 4.],
                      [1., 0., 3., 5.],
                      [2., 3., 0., 0.],
                      [4., 5., 0., 0.]])
        alignment = np.array([[0, 2],
                              [2, 1],
                              [1, 3],
                              [3, 0]])
        permuted = np.array([[0, 0, 4, 5],
                             [0, 0, 2, 3],
                             [4, 2, 0, 1],
                             [5, 3, 1, 0]])
        np.testing.assert_equal(permuted, wla.apply_alignment(g, alignment))


class TestWLalign(TestCase):
    def test_length_wl_signature(self):
        k = np.random.randint(10) + 1
        l = np.random.randint(10) + 1

        s = 0
        for i in range(l + 1):
            s += k ** i

        np.testing.assert_equal(s, wla.length_wl_signature(k, l))

        with np.testing.assert_raises(ValueError):
            wla.length_wl_signature(-1, 1)

        with np.testing.assert_raises(ValueError):
            wla.length_wl_signature(1, -1)

        with np.testing.assert_raises(ValueError):
            wla.length_wl_signature(0, 1)

        with np.testing.assert_raises(ValueError):
            wla.length_wl_signature(1, 0)

    def test_wl_signature(self):
        # Same example as figure 2 from the paper
        # Nodes: u v1 v2 v3 w1 w2 w3 w4 w5 w6
        g = np.zeros((11, 11))
        g[0, 1] = 25.  # a1
        g[0, 2] = 20.  # a2
        g[0, 3] = 1.  # a3

        g[1, 4] = 15.  # b1
        g[1, 5] = 14.  # b2
        g[1, 6] = 1.  # b3

        g[2, 7] = 40.  # b4
        g[2, 8] = 39.  # b5
        g[2, 9] = 1.  # b6

        g += g.T  # no need to fix the diagonal as it is zero

        def vol(i):
            return np.sum(g[i, :])

        k = 2
        l = 2
        s = np.zeros(wla.length_wl_signature(k, l))

        s[0] = vol(0)

        s[1] = vol(2) * g[0, 2] / vol(0)
        s[2] = vol(1) * g[0, 1] / vol(0)

        s[3] = vol(7) * (g[2, 7] / vol(2)) * (g[0, 2] / vol(0))
        s[4] = vol(8) * (g[2, 8] / vol(2)) * (g[0, 2] / vol(0))
        s[5] = vol(0) * (g[1, 0] / vol(1)) * (g[0, 1] / vol(0))
        s[6] = vol(4) * (g[1, 4] / vol(1)) * (g[0, 1] / vol(0))

        sig = wla.signature_wl(g, k, l, 0)
        np.testing.assert_almost_equal(s, sig)

        volumes = np.array([vol(i) for i in range(11)])

        sig = wla.signature_wl(g, k, l, 0, list(volumes))
        np.testing.assert_almost_equal(s, sig)

        volumes = volumes[:-1]
        with np.testing.assert_raises(ValueError):
            wla.signature_wl(g, k, l, 0, list(volumes))

    def test_wl_align(self):
        # Same example as figure 2 from the paper
        # Nodes: u v1 v2 v3 w1 w2 w3 w4 w5 w6
        g1 = np.zeros((11, 11))
        g1[0, 1] = 25.  # a1
        g1[0, 2] = 20.  # a2
        g1[0, 3] = 1.  # a3

        g1[1, 4] = 15.  # b1
        g1[1, 5] = 14.  # b2
        g1[1, 6] = 1.  # b3

        g1[2, 7] = 40.  # b4
        g1[2, 8] = 39.  # b5
        g1[2, 10] = 1.  # b6

        g1 += g1.T  # no need to fix the diagonal as it is zero

        k = 2
        l = 2

        alignment = np.zeros((11, 2), dtype=np.int32)
        alignment[:, 0] = np.arange(11, dtype=np.int32)
        alignment[:, 1] = np.random.permutation(11).astype(np.int32)

        g2 = wla.apply_alignment(g1, alignment)

        computed = wla.wl_align(g1, g2, k, l)
        np.testing.assert_array_equal(alignment, computed)

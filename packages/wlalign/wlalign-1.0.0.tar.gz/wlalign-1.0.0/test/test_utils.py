import os
import tempfile
from unittest import TestCase

import numpy as np

from wlalign import utils as wlu


class TestLoad(TestCase):
    def test_load_network(self):
        g = np.array([[0., 1., 2., 4.],
                      [1., 0., 3., 5.],
                      [2., 3., 0., 0.],
                      [4., 5., 0., 0.]])
        tf = tempfile.NamedTemporaryFile(suffix='.txt', mode='w')

        np.savetxt(tf.name, g)
        np.testing.assert_array_almost_equal(g, wlu.load_network(tf.name))

        delimiter = ','
        skip = '!'
        np.savetxt(tf.name, g, delimiter=delimiter, comments=skip,
                   header='comment')
        loaded = wlu.load_network(tf.name, skip=skip, delimiter=delimiter)
        np.testing.assert_array_almost_equal(g, loaded)


class TestWrite(TestCase):
    def test_check_can_write_file(self):
        # file exists AND file does not have write permission
        # with tempfile.NamedTemporaryFile() as tf:
        #     os.chmod(tf.name, 0o444)  # read only
        #     with self.assertRaises(PermissionError):
        #         cli.utils.check_can_write_file(fpath=tf.name)

        # file exists AND file has write permission AND no force
        with tempfile.NamedTemporaryFile() as tf:
            os.chmod(tf.name, 0o777)  # can write
            with self.assertRaises(FileExistsError):
                wlu.check_can_write_file(fpath=tf.name, force=False)

        # file exists AND file has write permission AND force
        with tempfile.NamedTemporaryFile() as tf:
            os.chmod(tf.name, 0o777)  # can write
            r = wlu.check_can_write_file(fpath=tf.name, force=True)
            self.assertTrue(r is None)

        # file does not exist AND directory does not exist
        with tempfile.TemporaryDirectory() as td:
            f = os.path.join(td, 'x', 'y')
            with self.assertRaises(FileNotFoundError):
                wlu.check_can_write_file(fpath=f)

        # file does not exist AND directory exists AND directory does not have
        # writing permission
        # with tempfile.TemporaryDirectory() as td:
        # os.chmod(td, 0o444)
        # f = os.path.join(td, 'x')
        # with self.assertRaises(PermissionError):
        #     cli.utils.check_can_write_file(fpath=f)

        # file does not exist AND directory exists AND directory has writing
        # permission
        with tempfile.TemporaryDirectory() as td:
            os.chmod(td, 0o777)
            f = os.path.join(td, 'x')
            r = wlu.check_can_write_file(fpath=f)
            self.assertTrue(r is None)


class TestCheckIs(TestCase):
    def test_check_is_adj(self):
        with np.testing.assert_raises(ValueError):
            g = np.random.rand(5, 6)
            wlu.check_is_adj(g)

        with np.testing.assert_raises(ValueError):
            g = np.random.rand(5, 5, 1)
            wlu.check_is_adj(g)

    def test_check_is_alignment(self):
        with np.testing.assert_raises(ValueError):
            a = np.random.rand(10, 2, 1)
            wlu.check_is_alignment(a)

        with np.testing.assert_raises(ValueError):
            a = np.random.rand(10, 3)
            wlu.check_is_alignment(a)

        with np.testing.assert_raises(ValueError):
            n = 10
            a = np.random.rand(n + 1, 2)
            wlu.check_is_alignment(a, n=n)

        with np.testing.assert_raises(ValueError):
            n = 10
            a = np.zeros((n, 2))
            a[:, 0] = np.arange(n)
            a[:, 1] = np.random.permutation(n)
            a[0, 1] += 1
            wlu.check_is_alignment(a)

    def test_check_compatible(self):
        with np.testing.assert_raises(ValueError):
            n = 10
            g1 = np.random.rand(n, n)
            g2 = np.random.rand(n + 1, n + 1)
            wlu.check_compatible_adj(g1, g2)


class TestSymmetrize(TestCase):
    def test_symmetrize(self):
        g = np.array([[0, 1, 2],
                      [0, 0, 3],
                      [0, 0, 0]])
        gs = np.array([[0, 1, 2],
                       [1, 0, 3],
                       [2, 3, 0]])

        np.testing.assert_array_almost_equal(gs, wlu.symmetrize_adj(g))

        g = np.array([[100, 1, 2],  # test the diagonal elements
                      [0, 0, 3],
                      [0, 0, 0]])
        gs = np.array([[100, 1, 2],
                       [1, 0, 3],
                       [2, 3, 0]])

        np.testing.assert_array_almost_equal(gs, wlu.symmetrize_adj(g))

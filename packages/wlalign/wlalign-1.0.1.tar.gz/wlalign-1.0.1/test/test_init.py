from unittest import TestCase

import wlalign


class TestNamespace(TestCase):
    def test_names(self):
        d = dir(wlalign)
        self.assertTrue('__version__' in d)

        self.assertTrue('alignment' in d)
        self.assertTrue('similarity' in d)
        self.assertTrue('utils' in d)

        self.assertTrue('apply_alignment' in d)
        self.assertTrue('length_wl_signature' in d)
        self.assertTrue('permutation_from_alignment' in d)
        self.assertTrue('signature_wl' in d)
        self.assertTrue('wl_align' in d)

        self.assertTrue('graph_jaccard_index' in d)
        self.assertTrue('gji' in d)

        self.assertTrue('load_network' in d)
        self.assertTrue('symmetrize_adj' in d)


import pandas as pd
import numpy as np
import os
import unittest

from descriptors import Descriptors
from ProAct import ProAct
from PyBioMed.PyBioMed.PyProtein import AAComposition, Autocorrelation, CTD, ConjointTriad, QuasiSequenceOrder, PseudoAAC
import utils as utils

class DescriptorTests(unittest.TestCase):

    def setUp(self):

        try:
            self.test_dataset1 = pd.read_csv(os.path.join('tests','test_data','test_thermostability.txt'),sep=",", header=0)
        except:
            raise IOError('Error reading in test_dataset1')
        try:
            self.test_dataset2 = pd.read_csv(os.path.join('tests','test_data','test_enantioselectivity.txt'),sep=",", header=0)
        except:
            raise IOError('Error reading in test_dataset2')
        try:
            self.test_dataset3 = pd.read_csv(os.path.join('tests','test_data','test_localization.txt'),sep=",", header=0)
        except:
            raise IOError('Error reading in test_dataset3')
        try:
            self.test_dataset4 = pd.read_csv(os.path.join('tests','test_data','test_absorption.txt'),sep=",", header=0)
        except:
            raise IOError('Error reading in test_dataset4')

    def test_descriptor(self):

        desc = Descriptors(self.test_dataset1['sequence'])
        print('here')
        gaps_test = utils.remove_gaps(desc.protein_seqs)
        print('gaps',gaps_test)

        self.assertIsNone(gaps_test)

        invalid_testdata1_copy = self.test_dataset1.append(['J,O,U,Z'])

        with self.assertRaises(ValueError):
            fail_desc = Descriptors(invalid_testdata1_copy)


        invalid_testdata1_copy[0]
        invalid_seqs = utils.valid_sequence(self.protein_seqs)
        if invalid_seqs!=None:
            raise ValueError('Invalid Amino Acids found in protein sequence dataset: {}'.format(invalid_seqs))

    def tearDown(self):

        del self.test_dataset1
        del self.test_dataset2
        del self.test_dataset3
        del self.test_dataset4


    # def test_aacomposition(self):
    #
    #     print('Testing AA Composition Descriptor....')
    #     desc = Descriptors(self.test_dataset1['sequence'])
    #
    #     aa_comp = desc.get_aa_composition()
    #
    #     self.assertIsInstance(aa_comp, pd.DataFrame)
    #     self.assertTrue('-' not in desc.protein_seqs)
    #     self.assertEqual(AAComposition.AALetter, list(aa_comp.columns))
    #
    #     #self.assert(aa_comp_df_keys == [] )
    #     #self.assert(aa_comp[1;10] == type(float))
    #     #pd.testing.assert_frame_equal(my_df, expected_df)
    #
    #     #assert concatenation of 2 descriptors works
    #     # self.assertEqual(aa_comp.shape == (self.test_dataset1.shape[0], 20))
    #
    # def test_dipeptidecomposition(self):
    #
    #     print('Testing Dipeptide Composition Descriptor....')

    #     # desc = Descriptors(self.test_dataset1['sequence'])
    #     #
    #     # dipeptide_comp = desc.get_dipeptide_composition()
    #     #
    #     # self.assertIsInstance(dipeptide_comp, pd.DataFrame)
    #     # self.assertTrue('-' not in desc.protein_seqs)
    #     #
    #     # self.ass
    #     # self.assertEqual(dipeptide_comp.shape == (self.test_dataset1.shape[0], X))
    #
    #     pass
    #
    # def test_tripeptidecomposition(self):

    #     print('Testing Tripeptide Composition Descriptor....')

    #     pass
    #
    # def test_normalized_moreaubroto_autocorrelation(self):
    #     print('Testing Normalised MoreauBroto Autocorrelation Descriptor....')

    #     pass
    #
    # def test_ctd(self):
    #     print('Testing CTD Descriptor....')

    #     pass
    #
    # def test_conjoint_triad(self):
    #     print('Testing Conjoint Triad Descriptor....')

    #     pass
    #
    # def test_seq_order_coupling_number(self):
    #     print('Testing Sequence Order Coupling Number Descriptor....')

    #     pass
    #
    # def test_quasi_seq_order(self):
    #     print('Testing Quasi Sequence Order Descriptor....')
    #     pass
    #
    # def test_pseudo_AAC(self):
    #     print('Testing Pseudo Amino Acid Composition Descriptor....')
    #     pass
    #
    # def test_amp_pseudo_AAC(self):
    #     print('Testing Amphiphilic Amino Acid Composition Descriptor....')

    #     pass
    #
    # def test_get_descriptor_encoding(self):
    #
    #     # def get_descriptor_encoding(self,descriptor):
    #
    #     pass
    #
    # def test_all_descriptors(self):
    #     print('Testing All Descriptors Functionality....')

    #     pass
    #     # def all_descriptors_list(self, descCombo=1):
    #
    # def test_valid_descriptors(self):
    #     print('Testing Valid Descriptor....')
    #     pass










# https://www.python.org/dev/peps/pep-0008/#module-level-dunder-names

#assert desc.all_descriptors.shape == []
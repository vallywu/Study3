"""
Test that batch and run-order correction behaves sensibly with a combination of synthetic and model datasets.
"""

import scipy
import pandas
import numpy
import seaborn as sns
import sys
import unittest
import os

sys.path.append("..")
import nPYc
from generateTestDataset import generateTestDataset

class test_rocorrection(unittest.TestCase):
	"""
	Use stored and synthetic datasets to validate run-order correction.
	"""

	def test_correctmsdataset_parallelisation(self):
		"""
		Check that parallel and single threaded code paths return the same result.
		"""

		noSamp = numpy.random.randint(500, high=2000, size=None)
		noFeat = numpy.random.randint(50, high=100, size=None)

		msData = generateTestDataset(noSamp, noFeat, dtype='MSDataset')

		correctedDataP = nPYc.batchAndROCorrection.correctMSdataset(msData, parallelise=True)
		correctedDataS = nPYc.batchAndROCorrection.correctMSdataset(msData, parallelise=False)

		numpy.testing.assert_array_almost_equal(correctedDataP.fit, correctedDataS.fit, err_msg="Serial and parallel fits not equal.")

		numpy.testing.assert_array_almost_equal(correctedDataP.intensityData, correctedDataS.intensityData, err_msg="Serial and parallel corrected data not equal.")


class test_rocorrection_sythetic(unittest.TestCase):

	def setUp(self):
		##
		# Generate synthetic data
		##
		#Use a random number of samples
		noSamples = numpy.random.randint(100, high=500, size=None)

		# Genreate monotonically increasing data
		self.testD = numpy.linspace(1,10, num=noSamples)

		# Generate run order
		self.testRO = numpy.linspace(1,noSamples, num=noSamples, dtype=int)

		# Build SR mask, and make sure first and last samples are references
		self.testSRmask = numpy.zeros_like(self.testD, dtype=bool)
		self.testSRmask[0:noSamples:7] = True
		self.testSRmask[:2] = True
		self.testSRmask[-2:] = True


	def test_runOrderCompensation_synthetic(self):
		"""
		Testing unpacking of parameters for RO correction.
		(only testing LOWESS at present)
		"""

		(corrected,fit) = nPYc.batchAndROCorrection._batchAndROCorrection.runOrderCompensation(self.testD,
																							self.testRO,
																							self.testSRmask,
																							{'window':11, 'method':'LOWESS'})

		numpy.testing.assert_array_almost_equal(self.testD, fit)
		numpy.testing.assert_array_almost_equal(numpy.std(corrected), 0.)


	def test_doLOESScorrection_synthetic(self):
		"""
		Correction of a monotonically increasing trend should be essentially perfect.
		"""

		(corrected,fit) = nPYc.batchAndROCorrection._batchAndROCorrection.doLOESScorrection(self.testD[self.testSRmask],
																							self.testRO[self.testSRmask],
																							self.testD,
																							self.testRO,
																							window=11)

		numpy.testing.assert_array_almost_equal(self.testD, fit)
		numpy.testing.assert_array_almost_equal(numpy.std(corrected), 0.)


	def test_batchCorrection_sythetic(self):

		# We need at least two features - pick which randomly
		testD2 = numpy.array([self.testD, self.testD]).T
		featureNo = numpy.random.randint(0, high=1, size=None)

		output = nPYc.batchAndROCorrection._batchAndROCorrection._batchCorrection(testD2,
																				self.testRO,
																				self.testSRmask,
																				numpy.ones_like(self.testRO),
																				[featureNo],
																				{'align':'mean', 'window':11, 'method':'LOWESS'},
																				0)

		featureNo_out = output[featureNo][0]
		corrected = output[featureNo][1]
		fit = output[featureNo][2]

		self.assertEqual(featureNo, featureNo_out)

		numpy.testing.assert_array_almost_equal(self.testD, fit)
		numpy.testing.assert_array_almost_equal(numpy.std(corrected), 0.)


class test_batchcorrection(unittest.TestCase):
	"""
	Test alignment of batch offsets
	"""

	def setUp(self):
		##
		# Generate synthetic data
		##
		#Use a random number of samples
		noSamples = numpy.random.randint(100, high=500, size=None)

		# Generate run order
		self.testRO = numpy.linspace(1,noSamples, num=noSamples, dtype=int)
		
		# Generate batches
		self.batch = numpy.ones(noSamples)
		splitPoint = numpy.random.randint(noSamples / 4., noSamples / 2., size=None)
		self.batch[splitPoint:] = self.batch[splitPoint:] + 1

		# Build SR mask, and make sure first and last samples are references
		self.testSRmask = numpy.zeros(noSamples, dtype=bool)
		self.testSRmask[0:noSamples:7] = True
		self.testSRmask[:2] = True
		self.testSRmask[-2:] = True

		# Generate normally distributed separately for each batch
		self.testD = numpy.zeros(noSamples)
		batches = list(set(self.batch))
		for batch in batches:
			batchMask = numpy.squeeze(numpy.asarray(self.batch == batch, 'bool'))
			noSamples = sum(batchMask)
	
			batchMean = numpy.random.randn(1) * numpy.random.randint(1, 1000, size=None)
			sigma = numpy.random.randn(1)
			self.testD[batchMask] = sigma * numpy.random.randn(noSamples) + batchMean


	def test_batchCorrection_sythetic(self):
		"""
		Check we can correct the offset in averages of two normal distributions
		"""
		# We need at least two features - pick which randomly
		testD2 = numpy.array([self.testD, self.testD]).T
		featureNo = numpy.random.randint(0, high=1, size=None)

		with self.subTest(msg='Checking alignment to mean'):
			overallMean = numpy.mean(self.testD[self.testSRmask])

			output = nPYc.batchAndROCorrection._batchAndROCorrection._batchCorrection(testD2,
																					self.testRO,
																					self.testSRmask,
																					self.batch,
																					[featureNo],
																					{'align':'mean', 'window':11, 'method':None},
																					0)

			means = list()
			batches = list(set(self.batch))
			for batch in batches:
				feature = output[featureNo][1]
				means.append(numpy.mean(feature[(self.batch == batch) & self.testSRmask]))

			numpy.testing.assert_allclose(means, overallMean)

		with self.subTest(msg='Checking alignment to median'):
			overallMedian = numpy.median(self.testD[self.testSRmask])

			output = nPYc.batchAndROCorrection._batchAndROCorrection._batchCorrection(testD2,
																					self.testRO,
																					self.testSRmask,
																					self.batch,
																					[featureNo],
																					{'align':'median', 'window':11, 'method':None},
																					0)

			medians = list()
			batches = list(set(self.batch))
			for batch in batches:
				feature = output[featureNo][1]
				medians.append(numpy.median(feature[(self.batch == batch) & self.testSRmask]))

			numpy.testing.assert_allclose(medians, overallMedian)


		def test_correctMSdataset_raises(self):

			with self.subTest(msg='Object type'):
				self.assertRaises(TypeError, nPYc.batchAndROCorrection.correctMSdataset, 's')

			with self.subTest(msg='Parallelise type'):
				dataset = nPYc.MSDataset('', type='empty')
				self.assertRaises(TypeError, nPYc.batchAndROCorrection.correctMSdataset, dataset, parallelise=1)


if __name__ == '__main__':
	unittest.main()

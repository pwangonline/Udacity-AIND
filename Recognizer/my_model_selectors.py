import math
import statistics
import warnings

import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import KFold
from asl_utils import combine_sequences


class ModelSelector(object):
	'''
	base class for model selection (strategy design pattern)
	'''

	def __init__(self, all_word_sequences: dict, all_word_Xlengths: dict, this_word: str,
				 n_constant=3,
				 min_n_components=2, max_n_components=10,
				 random_state=14, verbose=False):
		self.words = all_word_sequences
		self.hwords = all_word_Xlengths
		self.sequences = all_word_sequences[this_word]
		self.X, self.lengths = all_word_Xlengths[this_word]
		self.this_word = this_word
		self.n_constant = n_constant
		self.min_n_components = min_n_components
		self.max_n_components = max_n_components
		self.random_state = random_state
		self.verbose = verbose

	def select(self):
		raise NotImplementedError

	def base_model(self, num_states):
		# with warnings.catch_warnings():
		warnings.filterwarnings("ignore", category=DeprecationWarning)
		# warnings.filterwarnings("ignore", category=RuntimeWarning)
		try:
			hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
									random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
			if self.verbose:
				print("model created for {} with {} states".format(self.this_word, num_states))
			return hmm_model
		except:
			if self.verbose:
				print("failure on {} with {} states".format(self.this_word, num_states))
			return None


class SelectorConstant(ModelSelector):
	""" select the model with value self.n_constant

	"""

	def select(self):
		""" select based on n_constant value

		:return: GaussianHMM object
		"""
		best_num_components = self.n_constant
		return self.base_model(best_num_components)


class SelectorBIC(ModelSelector):
	""" select the model with the lowest Baysian Information Criterion(BIC) score

	http://www2.imm.dtu.dk/courses/02433/doc/ch6_slides.pdf
	Bayesian information criteria: BIC = -2 * logL + p * logN
	"""

	def select(self):
		""" select the best model for self.this_word based on
		BIC score for n between self.min_n_components and self.max_n_components

		:return: GaussianHMM object
		"""
		warnings.filterwarnings("ignore", category=DeprecationWarning)

		# TODO implement model selection based on BIC scores
		# raise NotImplementedError
		bestBIC = float("-inf")
		bestModel = None
		for n_comp in range(self.min_n_components, self.max_n_components):
			try:
				if n_comp > len(self.sequences):
					continue
				model = self.base_model(n_comp)
				logL = model.score(self.X, self.lengths)
				bic = -2 * logL + (n_comp + n_comp * (n_comp -1) + n_comp * model.n_features * 2) + math.log(len(
					self.sequences))
				if bic > bestBIC:
					bestBIC = bic
					bestModel = model
			except:
				continue
		# print(self.this_word)
		# print(bestBIC)
		return bestModel

class SelectorDIC(ModelSelector):
	''' select best model based on Discriminative Information Criterion

	Biem, Alain. "A model selection criterion for classification: Application to hmm topology optimization."
	Document Analysis and Recognition, 2003. Proceedings. Seventh International Conference on. IEEE, 2003.
	http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.6208&rep=rep1&type=pdf
	DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))
	'''

	def select(self):
		warnings.filterwarnings("ignore", category=DeprecationWarning)

		# TODO implement model selection based on DIC scores
		# raise NotImplementedError
		bestDIC = float("-inf")
		bestModel = None
		for n_comp in range(self.min_n_components, self.max_n_components):
			otherLogL = 0
			try:
				model = self.base_model(n_comp)
				logL = model.score(self.X, self.lengths)
				for word in self.hwords:
					if word is self.this_word:
						continue
					X, length = self.hwords[word]
					otherLogL += model.score(X, length)
				otherLogL /= float(len(self.hwords) -1)
				dic = logL - otherLogL
				if dic > bestDIC:
					bestDIC = dic
					bestModel = model
			except:
				continue
		# print(self.this_word)
		# print(bestDIC)
		return bestModel


class SelectorCV(ModelSelector):
	''' select best model based on average log Likelihood of cross-validation folds

	'''

	def select(self):
		warnings.filterwarnings("ignore", category=DeprecationWarning)

		# TODO implement model selection using CV
		# raise NotImplementedError
		bestLogL = float("-inf")
		bestModel = None
		bestComp = None
		for n_comp in range(self.min_n_components, self.max_n_components):
			logLs = []
			if n_comp > len(self.sequences):
				continue
			try:
				split_method = KFold(n_splits=n_comp)
				for cv_train_idx, cv_test_idx in split_method.split(self.sequences):
					train_X, train_lengths = combine_sequences(cv_train_idx, self.sequences)
					model = GaussianHMM(n_components=n_comp, covariance_type="diag", n_iter=1000,
					            random_state=self.random_state, verbose=False).fit(train_X, train_lengths)
					test_X, test_lengths = combine_sequences(cv_test_idx, self.sequences)
					logLs.append(model.score(test_X, test_lengths))
					logL = sum(logLs) / float(len(logLs))
				if logL > bestLogL:
					bestLogL = logL
					bestComp = n_comp
			except:
				continue
		try:
			bestModel = GaussianHMM(n_components=bestComp, covariance_type="diag", n_iter=1000, random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
			bestLogL = bestModel.score(self.X, self.lengths)
		except:
			bestLogL = float('-inf')
		# print(self.this_word)
		# print(bestLogL)
		return bestModel


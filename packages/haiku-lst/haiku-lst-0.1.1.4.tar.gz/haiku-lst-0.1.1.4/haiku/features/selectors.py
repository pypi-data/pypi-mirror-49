import operator, math
from functools import reduce

#---------------------------------------------------------------------------
# feature selector factory
#---------------------------------------------------------------------------
class FeatureSelectror (object):
	def __init__ (self, tokenCount, docCount, total_tokenCount, total_docCount, total_poolCount):
		self.docCount = docCount
		self.tokenCount = tokenCount
		self.total_docCount = total_docCount
		self.total_poolCount = total_poolCount		
		self.total_tokenCount = total_tokenCount		
	
	def __repr__ (self):
		return '<Base Selector: %d, %d>' % (self.total_docCount, self.total_poolCount)
	
	def __call__ (self, stat):
		return self.compute (stat)
		
	def compute (self, stat):
		I = []		
		sum = reduce (operator.add, [_f [1] for _f in stat])		
		for i in range (self.total_poolCount):
			freq, appr = stat [i]
			A = appr
			B = sum - A
			C = self.docCount [i] - A
			D = self.total_docCount - (A + B + C)
			result = self.claculate (A, B, C, D)
			I.append (result)
		return self.method (I)
	
	def method (self, I):
		return self.max (I)	
		
	def max (self, I):
		return max (I)
		
	def sd (self, I):
		avg = self.avg (I)
		return math.sqrt (reduce (operator.add, [(x - avg) ** 2 for x in I]) / self.total_poolCount)
	
	def cv (self, I):
		avg = self.avg (I)
		sd = self.sd (I)
		return sd / avg
		
	def avg (self, I):
		return (reduce (operator.add, I)) / len (I)
	
	def asis (self, I):
		return I	
		
class mutual_information (FeatureSelectror):
	def method (self, I):
		return self.sd (I)	
		
	def claculate (self, A, B, C, D):		
		"""
		      1 + (A x N)
		log ---------------
		     (A+C) x (A+B)	
		"""
		r= math.log (1 + float (A * self.total_docCount) / ((A + C) * (A + B)))		
		return r

class chi2statistics (FeatureSelectror):
	def method (self, I):
		return self.max (I)
		
	def claculate (self, A, B, C, D):		
		"""
		      N x (AD - CB)^2
		-----------------------------
		(A+C) x (B+D) x (A+B) x (C+D)	
		"""
		upper = self.total_docCount * ((A * D - C * B) ** 2)
		lower = (A+C) * (B+D) * (A+B) * (C+D)		
		return float (upper) / lower

class dice_coefficient (FeatureSelectror):
	def claculate (self, A, B, C, D):
		return (2. * A) / (2 * A + B + C)		

class jaccard_coefficient (FeatureSelectror):		
	def claculate (self, A, B, C, D):
		return float(A) / (A + B + C)
	
class category_frequency (FeatureSelectror):
	def compute (self, stat):		
		CF = len ([_f for _f in stat if _f [0]])
		result = []
		for i in range (self.total_poolCount):
			freq, appr = stat [i]
			if not freq:
				result.append (0)
			else:
				W = freq * (math.log (self.total_poolCount) - math.log (CF) + 1)
				result.append (W)		
		return self.method (result)
	
class document_frequency (category_frequency):
	def compute (self, stat):
		DF = reduce (operator.add, [_f [1] for _f in stat])
		result = []
		for i in range (self.total_poolCount):
			freq, appr = stat [i]
			if not freq:
				result.append (0.0)
			else:
				W = freq * (math.log (self.total_docCount) - math.log (DF) + 1)
				result.append (W)
		return self.method (result)

class oddsratio (category_frequency):
	def compute (self, stat):
		"""
		      P(W|C1) (1-P(W|C2))
		log -----------------------
		      (1-P(W|C1)) P(W|C2)
		      
		odds(W) = (1/n^2) / (1 - 1/n^2) ; p(W) = 0
		        = (1 - 1/n^2) / (1/n^2); P(W) = 1
		        = P(W) / (1 - P(W)) ; P(W) != 0 and P(W) != 1 
		"""
		result = []
		T = reduce (operator.add, [_f [0] for _f in stat])
		for i in range (self.total_poolCount):
			targetClassSize = self.tokenCount [i]
			freq, appr = stat [i]
			otherClassSize = (self.total_tokenCount - self.tokenCount [i])
			count1 = float (freq)
			count2 = float (T - freq)
			P_pos = float(count1) / targetClassSize
			P_neg = float(count2) / otherClassSize
			odds_pos = self.calculate (P_pos, count1, targetClassSize)
			odds_neg = self.calculate (P_neg, count2, otherClassSize)
			odds_ratio = math.log (odds_pos / odds_neg)
			result.append (odds_ratio)
		return self.method (result)
	
	def calculate (self, P, count, size):		
		if P == 0.: 
			odds = (0.99 / size ** 2) / (1 - 0.99 / size ** 2)
		elif P == 1.: 
			odds = (1 - 0.99 / size ** 2) / (0.99 / size ** 2)
		else: 
			odds = (float (count) / size) / (1 - (float (count) / size))
		return odds

class freqlogp (oddsratio):
	def compute (self, stat):
		"""
		                P(W|C1)
		Freq(W) x log -----------
		                P(W|C2)		
		"""
		result = []
		T = reduce (operator.add, [_f [0] for _f in stat])
		for i in range (self.total_poolCount):
			targetClassSize = self.tokenCount [i]
			freq, appr = stat [i]
			otherClassSize = (self.total_tokenCount - self.tokenCount [i])
			count1 = float (freq)
			count2 = float (T - freq)
			P_pos = float(count1) / targetClassSize
			P_neg = float(count2) / otherClassSize
			P_pos = self.calculate (P_pos, count1, targetClassSize)
			P_neg = self.calculate (P_neg, count2, otherClassSize)
			freq_log_p = count1 * math.log (P_pos / P_neg)
			result.append (freq_log_p)
		return self.method (result)
	
	def calculate (self, P, count, size):
		if P == 0.: 
			prob = (1. / size ** 2)
		elif P == 1.: 
			prob = (1 - 0.99 / size ** 2)
		else: 
			prob = (float (count) / size)
		return prob
		
class information_gain (FeatureSelectror):
	def compute (self, stat):
		"""
		G(t) = -SIGMA P(Ci) * log P(Ci)
			   +P(t) * SIGMA P(Ci|t) * log P(Ci|t)
			   +P(-t) * SIGMA P(Ci|-t) * log P(Ci|-t)	
		"""
		TOTAL_FREQ = reduce (operator.add, [_f [0] for _f in stat])
		TOTAL_APPR = reduce (operator.add, [_f [1] for _f in stat])		
		pc = 0.
		pt_pos = 0.
		pt_neg = 0.		
		for i in range (self.total_poolCount):
			freq, appr = stat [i]
			pc += self.docCount [i] / self.total_docCount
			pt_pos += appr / TOTAL_APPR
			pt_neg += (self.docCount [i] - appr) / (self.total_docCount - TOTAL_APPR)
		
		IG = -1. * self.calculate (pc) \
		+ (TOTAL_FREQ / self.total_tokenCount) * self.calculate (pt_pos) \
		+ ((self.total_tokenCount - TOTAL_FREQ) / self.total_tokenCount) * self.calculate (pt_neg)
		return IG
		
	def calculate (self, prob):
		if not prob: return 0.
		return prob * math.log (prob)	
		

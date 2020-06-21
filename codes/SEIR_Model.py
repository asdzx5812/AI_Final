import numpy as np

class SEIR_Model:

	STATES = ['SUSCEPTIBLE', 'EXPOSED', 'INFECTIOUS', 'RECOVERED', 'DEAD']
	SYMPTOMATIC_TRANS_PROB = 1.70834e-4
	ASYMPTOMATIC_TRANS_PROB = SYMPTOMATIC_TRANS_PROB / 2
	SYMPTOMATIC_PROB = 0.63 #0.0205 / 120 (1/min)
	DEAD_PROB = 0.006240867732 # 43.5 / 794 (1/day) 8~10 days is the infectious period
	QUARANTINE_PROB = 0
	MASK_PROTECTION_PROB = 0.292 # / 0.915
	WEARING_MASK_PROB = 0

	@staticmethod
	def getRandomIncubationPeriod(): # E -> Onset 潛伏期 2~14
		d = round(np.random.normal(loc=5, scale=0.5))
		while d < 2 or d > 14:
			d = round(np.random.normal(loc=5, scale=0.5))
		return d

	@staticmethod
	def getRandomLatentPeriod(incubation_period): # E -> I 潛藏期 1~3
		d = round(np.random.normal(loc=2, scale=0.5))
		while d < 1 or d > 3:
			d = round(np.random.normal(loc=2, scale=0.5))
		return incubation_period - d
	

	@staticmethod
	def getRandomInfectiousPeriod(): # I -> R 感染期 8~10
		d = round(np.random.normal(loc=9, scale=0.5))
		while d < 8 or d > 10:
			d = round(np.random.normal(loc=9, scale=0.5))
		return d


	@staticmethod
	def getRandomIllnessPeriod(): # 發病期 9~10
		d = round(np.random.normal(loc=9.5, scale=0.25))
		while d < 9 or d > 10:
			d = round(np.random.normal(loc=9.5, scale=0.25))
		return d



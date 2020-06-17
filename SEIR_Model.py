import random

class SEIR_Model:

	STATES = ['SUSCEPTIBLE', 'EXPOSED', 'INFECTIOUS', 'RECOVERED', 'DEAD']
	SYMPTOMATIC_TRANS_PROB = 1.70834e-4
	ASYMPTOMATIC_TRANS_PROB = SYMPTOMATIC_TRANS_PROB/2
	SYMPTOMATIC_PROB = 0.282094565# 0.6 #0.0205 / 120 (1/min)
	DEAD_PROB = (5.47869e-2)/4.5 # 43.5 / 794 (1/day) 3~6days is the infectious period

	@staticmethod
	def getRandomLatentPeriod(): # E -> I 潛藏期
		return random.randint(1, 2)

	@staticmethod
	def getRandomIncubationPeriod(latent_period): # E -> Outbreak 潛伏期
		return random.randint(0, 3 - latent_period)

	@staticmethod
	def getRandomContagiousPeriod(): # I -> R 感染期
		return random.randint(3, 6)


	


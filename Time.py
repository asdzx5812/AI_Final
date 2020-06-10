from datetime import datetime, timedelta
import random

class Time:

	@staticmethod
	def getRandomTimeStamp(s1, s2):
		t1 = datetime.strptime(s1, '%H:%M')
		t2 = datetime.strptime(s2, '%H:%M')

		return datetime.strftime(t1 + random.random()*(t2-t1), '%H:%M')

	@staticmethod
	def addMinutes(s1, m):
		t1 = datetime.strptime(s1, '%H:%M')
		# print (t1, type(t1))
		# print (t1+timedelta(minutes=m), type(t1+timedelta(minutes=m)))
		return datetime.strftime(t1+timedelta(minutes=m), '%H:%M')

	@staticmethod
	def isSmaller(s1, s2):
		t1 = datetime.strptime(s1, '%H:%M')
		t2 = datetime.strptime(s2, '%H:%M')
		return t1 < t2

	@staticmethod
	def isSmallerEqual(s1, s2):
		t1 = datetime.strptime(s1, '%H:%M')
		t2 = datetime.strptime(s2, '%H:%M')
		return t1 <= t2
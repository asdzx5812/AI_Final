import random
import mapmodule
import logging
import numpy as np
from Time import Time
from SEIR_Model import SEIR_Model

logging.basicConfig(level=logging.INFO)

####################################################################################################
##################################### Constants & Infomations ######################################
####################################################################################################

INF = 9999999999999999999
MOVING_SPEED = 500.0

START_POINTS_ID = [
	12, # 正門
	26, # 西門
	50, # 後門
	8, 	# 側門
	1, 	# 舟山門
	6,	# 長興街門
	54,	# 公館門
	55, # 新體門
	7, 	# 男六
	9  	# 大一女
]
BUILDINGS_ID = [
	41, # 新生 
	35, # 博雅
	29, # 普通
	10, # 共同
	53, # 新體
	99	# 系館
]
BUILDINGS_PROB_WEIGTS = [
	0.15,
	0.15,
	0.15,
	0.15,
	0.05,
	0.35
]

INSTITUTES_NAME = ['資工', '外文', '工管', '機械', '生傳', '政治', '法律']
INSTITUTES_ID = [
	40, # 德田館 
	22, # 文學院 
	0,  # 管一 
	32, # 工綜
	11,  # BICD
	48, # 社科院
	49  # 霖澤館
]

RESTAURANTS_ID = [
	25, # 活大
	30, # 小福
	2, 	# 小小福
	39, # 女九
	12, # 正門
	26, # 西門
	50, # 後門
	8, # 側門
	1, 	# 舟山門
	6,	# 長興街門
	54,	# 公館門
	9  # 大一女
]

CLASS_START_TIME = ['8:10', '9:10', '10:20', '11:20', '12:20', '13:20', '14:20', '15:30', '16:30', '17:30', '18:25']
CLASS_END_TIME = ['9:00', '10:00', '11:10', '12:10', '13:10', '14:10', '15:10', '16:20', '17:20', '18:20', '19:15']
SCHEDULE_STATE = ['IDLE', 'INCLASS', 'MOVING', 'NULL']

MAP = mapmodule.Map()

HEALTH_STATES = ['SUSCEPTIBLE', 'EXPOSED', 'INFECTIOUS', 'RECOVERED', 'DEAD']

####################################################################################################
########################################## Classes #################################################
####################################################################################################

class Schedule:
	def __init__(self, gender, instituteIdx):
		self.startPointID = self.getRandomStartPointID(gender)
		self.destPointsID = []
		self.destTimes = []

		self.arrangeSchedule(instituteIdx)
		self.arrangeRestaurant()

		self.newDayInit(0)

	def newDayInit(self, day):
		self.startTime = Time.getRandomTimeStamp(Time.addMinutes(self.destTimes[day][0], -30), Time.addMinutes(self.destTimes[day][0], -15)) # 上課前30~15分鐘
		self.endPointID = self.startPointID
		self.endTime = Time.getRandomTimeStamp(Time.addMinutes(self.destTimes[day][-1], 65), Time.addMinutes(self.destTimes[day][-1], 80	)) # 下課後15～30分鐘
		self.nextDestIdx = 0
		self.numDestPoints = len(self.destPointsID[day])
		
	def arrangeSchedule(self, instituteIdx): # Arrange Class Schedule
		for day in range(5):
			tmp_destPointsID = []
			tmp_destTimes = []
			i = 0
			while i < len(CLASS_START_TIME)-1: # 每次連續上兩節課
				if random.random() >= 0.5:
					destID = self.getRandomDestPointID()
					if destID == 99: # 系館
						destID = INSTITUTES_ID[instituteIdx]
					tmp_destPointsID.append(destID)
					tmp_destTimes.append(CLASS_START_TIME[i])
					i += 1
					if i < len(CLASS_START_TIME):
						tmp_destPointsID.append(destID)
						tmp_destTimes.append(CLASS_START_TIME[i])
				i += 1

			self.destPointsID.append(tmp_destPointsID)
			self.destTimes.append(tmp_destTimes)
			
	def arrangeRestaurant(self): # Arrange Restaraunt for lunch
		for day in range(5):
			i = 0
			while i < len(self.destTimes[day]) and Time.compare(self.destTimes[day][i], '<', '12:20'):
				i += 1
			# print ("i =",i)
			# print (self.destTimes[day][i])
			if i >= len(self.destTimes[day]) or self.destTimes[day][i] != '12:20':
				if i >= len(self.destTimes[day]):
					self.destPointsID[day].append(random.choice(RESTAURANTS_ID))
					self.destTimes[day].append('12:20')
				else:
					self.destPointsID[day] = self.destPointsID[day][:i] + [random.choice(RESTAURANTS_ID)] + self.destPointsID[day][i:]
					self.destTimes[day] = self.destTimes[day][:i] + ['12:20'] + self.destTimes[day][i:]

			elif i+1 >= len(self.destTimes[day]) or self.destTimes[day][i+1] != '13:20':
				if i+1 >= len(self.destTimes[day]):
					self.destPointsID[day].append(random.choice(RESTAURANTS_ID))
					self.destTimes[day].append('13:20')
				else:
					self.destPointsID[day] = self.destPointsID[day][:i+1] + [random.choice(RESTAURANTS_ID)] + self.destPointsID[day][i+1:]
					self.destTimes[day] = self.destTimes[day][:i+1] + ['13:20'] + self.destTimes[day][i+1:]
			
			elif i-1 < 0 or self.destTimes[day][i-1] != '11:20':
				if i-1 < 0:
					self.destPointsID[day] = [random.choice(RESTAURANTS_ID)] + self.destPointsID[day]
					self.destTimes[day] = ['11:20'] + self.destTimes[day]
				else:
					self.destPointsID[day] = self.destPointsID[day][:i] + [random.choice(RESTAURANTS_ID)] + self.destPointsID[day][i:]
					self.destTimes[day] = self.destTimes[day][:i] + ['11:20'] + self.destTimes[day][i:]
	
	def getRandomStartPointID(self, gender):
		start_point_id = random.choice(START_POINTS_ID)
		if gender == 'male':
			while start_point_id == 9: #大一女
				start_point_id = random.choice(START_POINTS_ID)
		else:
			while start_point_id == 7: #男六
				start_point_id = random.choice(START_POINTS_ID)
		return start_point_id

	def getRandomDestPointID(self):
		return random.choices(BUILDINGS_ID, weights=BUILDINGS_PROB_WEIGTS)[0]

	def print(self, day):
		print ('---------Schedule---------')
		print ('startPoint :', self.startPointID, MAP.point_list[self.startPointID].name)
		print ('startPointPosition :', MAP.point_list[self.startPointID].position)
		print ('startTime :', self.startTime)
		print ('destPoints :', self.destPointsID[day])
		for i in self.destPointsID[day]:
			print (MAP.point_list[i].name, end=' ')
		print ("")
		print ('destPointsPosition : ', end='')
		for i in self.destPointsID[day]:
			print (MAP.point_list[i].position, end='')
		print ("")
		print ('destTimes :', self.destTimes[day])
		print ('nextDestIdx :', self.nextDestIdx)
		print ('numDestPoints :', self.numDestPoints)
		print ('endPoint :', self.endPointID, MAP.point_list[self.endPointID].name)
		print ('endTime: ', self.endTime)
		print ('--------------------------')


class HealthState:
	def __init__(self):
		self.state = 'SUSCEPTIBLE'
		self.latentPeriod = SEIR_Model.getRandomLatentPeriod() # 潛藏期
		self.incubationPeriod = SEIR_Model.getRandomIncubationPeriod(self.latentPeriod) # 潛伏期
		self.contagiousPeriod = SEIR_Model.getRandomContagiousPeriod() # 感染期
		self.currentInfectedDay = 0
		self.currentProb = 0

	def newDayCheckState(self):

		if self.state == 'SUSCEPTIBLE':
			return

		self.currentInfectedDay += 1

		if self.currentInfectedDay <= self.incubationPeriod and random.random() <= SEIR_Model.SYMPTOMATIC_PROB: # 發病
			self.currentProb = SEIR_Model.SYMPTOMATIC_TRANS_PROB

		if self.state == 'EXPOSED' and self.currentInfectedDay > self.latentPeriod:
			self.state = 'CONTAGIOUS'
			self.currentPeriod = 0

		elif self.state == 'CONTAGIOUS' and self.currentInfectedDay > self.latentPeriod + self.contagiousPeriod:
			if random.random() <= SEIR_Model.DEATH_PROB:
				self.state = 'DEAD'
			else:
				self.state = 'RECOVERED'


class Student:
	def __init__(self, healthState='SUSCEPTIBLE'):
		self.gender = 'male' if random.choice([0, 1]) == 0 else 'female'
		self.instituteIdx = random.randint(0, len(INSTITUTES_NAME)-1)
		self.healthState = HealthState()
		self.scheduleState = 'NULL'
		self.schedule = Schedule(gender=self.gender, instituteIdx=self.instituteIdx)
		self.currentPointID = self.schedule.startPointID
		self.nextPointID = -1
		self.currentPosition = (MAP.point_list[self.schedule.startPointID].position).copy() # shallow copy
		self.currentSpeed = 0.0
		self.currentDirection = np.array([0.0, 0.0])

	def print(self, day):
		print ('--------------Student--------------')
		print ('gender :', self.gender)
		print ('institute :', INSTITUTES_ID[self.instituteIdx], INSTITUTES_NAME[self.instituteIdx])
		print ('healthState :', self.healthState)
		print ('scheduleState :', self.scheduleState)
		self.schedule.print(day)
		print ('currentPoint :', self.currentPointID, MAP.point_list[self.currentPointID].name)
		print ('nextPoint :', self.nextPointID, MAP.point_list[self.nextPointID].name)
		print ('currentPosition :', self.currentPosition)
		print ('currentSpeed :', self.currentSpeed)
		print ('currentDirection :', self.currentDirection)
		print ('-----------------------------------')

	def printPositionInfo(self, day):
		print ('--------------Student--------------')
		print ('scheduleState :', self.scheduleState)
		print ('currentPoint :', self.currentPointID, MAP.point_list[self.currentPointID].name)
		print ('currentPosition :', self.currentPosition)
		print ('nextPoint :', self.nextPointID, MAP.point_list[self.nextPointID].name)
		if self.schedule.nextDestIdx < self.schedule.numDestPoints:
			print ('nextDest : [', self.schedule.nextDestIdx, ']', MAP.point_list[self.schedule.destPointsID[day][self.schedule.nextDestIdx]].name)
		print ('currentSpeed :', self.currentSpeed)
		print ('currentDirection :', self.currentDirection)
		print ('-----------------------------------')

	def hasNextClass(self, CURRENT_TIME, day):
		idx = self.schedule.nextDestIdx
		return idx < self.schedule.numDestPoints and Time.compare(Time.addMinutes(CURRENT_TIME, 20), '>=', self.schedule.destTimes[day][idx])

	def timeToLeave(self, CURRENT_TIME):
		return Time.compare(Time.addMinutes(CURRENT_TIME, 15), '>=', self.schedule.endTime)

	def findNearestPointID(self, day):
		nearestPointID = None
		min_dist = INF
		for pointID in MAP.point_list[self.currentPointID].near_points:
			if self.schedule.nextDestIdx < self.schedule.numDestPoints:
				dist = MAP.point_list[pointID].dis_list[self.schedule.destPointsID[day][self.schedule.nextDestIdx]]
			else:
				dist = MAP.point_list[pointID].dis_list[self.schedule.endPointID]
			if dist < min_dist:
				min_dist = dist
				nearestPointID = pointID

		return nearestPointID

	def move(self, day):

		delta_distance = np.linalg.norm(self.currentSpeed * self.currentDirection)
	
		while delta_distance > 0:
			# print ('current Point:', self.currentPointID, self.currentPosition, 'next point:',  self.nextPointID, MAP.point_list[self.nextPointID].position)
			# print ("cur_Dir :", self.currentDirection, 'vs', (MAP.point_list[self.nextPointID].position - self.currentPosition) / np.linalg.norm(MAP.point_list[self.nextPointID].position - self.currentPosition))
				
			left_distance_to_next_point = np.linalg.norm(MAP.point_list[self.nextPointID].position - self.currentPosition)
			# print ("id :", self.currentPointID, MAP.point_list[self.currentPointID].name, '->', self.nextPointID,  MAP.point_list[self.nextPointID].name)
			#print ("dis =", delta_distance, left_distance_to_next_point)

			if delta_distance >= left_distance_to_next_point: 
				delta_distance -= left_distance_to_next_point

				self.currentPointID = self.nextPointID
				self.currentPosition = (MAP.point_list[self.currentPointID].position).copy()
				self.nextPointID = self.findNearestPointID(day)

				#print ("id ~ ", self.currentPointID, MAP.point_list[self.currentPointID].name, '->', self.nextPointID,  MAP.point_list[self.nextPointID].name)
				self.currentDirection = (MAP.point_list[self.currentPointID].unit_vec[self.nextPointID]).copy()

				#print ("!!!!!!", self.schedule.nextDestIdx, MAP.point_list[self.schedule.destPointsID[day][self.schedule.nextDestIdx]].name)
				if (self.schedule.nextDestIdx < self.schedule.numDestPoints and self.currentPointID == self.schedule.destPointsID[day][self.schedule.nextDestIdx]) \
					or (self.currentPointID == self.schedule.endPointID): # 到教室了
					logging.debug("Reach the point!!")
					break
				else:
					logging.debug("Turn to", self.currentPointID, MAP.point_list[self.currentPointID].name)
			
			else: # delta_distance < left_distance_to_next_point
				#assert ((self.currentDirection == (MAP.point_list[self.nextPointID].position - self.currentPosition) / np.linalg.norm(MAP.point_list[self.nextPointID].position - self.currentPosition)).all())
				self.currentPointID = -1
				self.currentPosition += self.currentDirection * delta_distance
				break

		#self.printPositionInfo(day)

	def Action(self, CURRENT_TIME, day):

		if self.healthState.state == 'DEAD':
			self.scheduleState = 'NULL'
			return

		if CURRENT_TIME in CLASS_END_TIME:
			logging.debug(f'====================={CURRENT_TIME}============================')
			# self.printPositionInfo(day)

		if Time.compare(CURRENT_TIME, '==', self.schedule.startTime): # 到學校了
			self.scheduleState = 'IDLE'
			self.currentPointID = self.schedule.startPointID
			self.currentPosition = (MAP.point_list[self.schedule.startPointID].position).copy()

		if self.scheduleState == 'IDLE':
			if self.hasNextClass(CURRENT_TIME, day) or (self.schedule.nextDestIdx == self.schedule.numDestPoints and self.timeToLeave(CURRENT_TIME)): # 該上課了
				self.scheduleState = 'MOVING'
				self.nextPointID = self.findNearestPointID(day)
				self.currentSpeed = MOVING_SPEED + random.uniform(-50, 50)
				self.currentDirection = (MAP.point_list[self.currentPointID].unit_vec[self.nextPointID]).copy()
			else:
				pass

		elif self.scheduleState == 'MOVING':

			self.move(day)

			if (self.schedule.nextDestIdx < self.schedule.numDestPoints and self.currentPointID == self.schedule.destPointsID[day][self.schedule.nextDestIdx]) \
				or (self.currentPointID == self.schedule.endPointID): # 到教室了/要離開學校了
				if self.schedule.nextDestIdx < self.schedule.numDestPoints:
					logging.debug(f'Reach the classroom!! --{CURRENT_TIME}')
					self.scheduleState = 'INCLASS'
					offset_x = MAP.point_list[self.currentPointID].offset[0]
					offset_y = MAP.point_list[self.currentPointID].offset[1]
					self.currentPosition[0] += random.uniform(offset_x, -offset_x)
					self.currentPosition[1] += random.uniform(offset_y, -offset_y)
					
				else :
					logging.debug(f'Bye bye!! --{CURRENT_TIME}')
					self.scheduleState = 'NULL'
				
				self.currentSpeed = 0.0
				self.currentDirection = np.array([0.0, 0.0])
				if self.schedule.nextDestIdx < self.schedule.numDestPoints:
					self.schedule.nextDestIdx += 1

				if self.healthState == 'INFECTIOUS':
					MAP.point_list[self.currentPointID].infect_prob += INFECT_PROB

		elif self.scheduleState == 'INCLASS':

			if CURRENT_TIME in CLASS_END_TIME: # 下課了
				logging.debug("Class ends --", CURRENT_TIME)
			
				if self.hasNextClass(CURRENT_TIME, day): # 下節有課
					logging.debug("I have next class :", self.schedule.nextDestIdx, MAP.point_list[self.schedule.destPointsID[day][self.schedule.nextDestIdx]].name)
					idx = self.schedule.nextDestIdx
					if self.schedule.destPointsID[day][idx] != self.schedule.destPointsID[day][idx-1]: # 下節課不同教室
						self.currentPosition = (MAP.point_list[self.currentPointID].position).copy()
						self.scheduleState = 'MOVING'

						self.nextPointID = self.findNearestPointID(day)
						self.currentSpeed = MOVING_SPEED + random.uniform(50, -50)
						self.currentDirection = (MAP.point_list[self.currentPointID].unit_vec[self.nextPointID]).copy()
					
						if self.healthState.state == 'INFECTIOUS':
							MAP.point_list[self.currentPointID].infect_prob -= self.healthState.currentProb

					else: # 下節同教室
						self.schedule.nextDestIdx += 1

				else: # 下節沒課
					self.currentPosition = (MAP.point_list[self.currentPointID].position).copy()
					self.scheduleState = 'IDLE'

					if self.healthState == 'INFECTIOUS':
						MAP.point_list[self.currentPointID].infect_prob -= self.healthState.currentProb

			else: # 上課中
				infect_prob = MAP.point_list[self.currentPointID].infect_prob
				if infect_prob > 0 and self.healthState == 'SUSCEPTIBLE':
					if random.random() <= infect_prob:
						self.healthState = 'INFECTIOUS'
			

	def newDayInit(self, day):
		self.schedule.newDayInit(day)
		self.healthState.newDayCheckState()


if __name__ == '__main__':

	day = 0
	student = Student()

	student = Student()

	for day in range(5):
		print ("day", day)
		student.newDayInit(day)
		student.print(day)
		CURRENT_TIME = '07:40'
		while Time.compare(CURRENT_TIME, '<=', '20:00'):
			# if CURRENT_TIME in CLASS_END_TIME:
			# 	print (CURRENT_TIME)
			student.Action(CURRENT_TIME, day)
			if student.scheduleState != 'NULL':
			# show him/her on the map
				pass
			else:
				# hide him/her on the map
				pass
			CURRENT_TIME = Time.addMinutes(CURRENT_TIME, 1)


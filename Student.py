import random
import mapmodule
import numpy as np
from Time import Time

INF = 9999999999999999999

HEALTH_STATES = ['HEALTHY', 'INFECTED']
INFECT_PROB = 1.70834e-4 #0.0205 / 120 (1 /min)

START_POINTS_ID = [
	7, 	# 正門
	26, # 西門
	50, # 後門
	13, # 側門
	1, 	# 舟山門
	11,	# 長興街門
	54,	# 公館門
	55, # 新體門
	12, # 男六
	14  # 大一女
]

BUILDINGS_ID = [
	41, # 新生 
	35, # 博雅
	29, # 普通
	5,  # 共同
	53, # 新體
	99	# 系館
]

INSTITUTES_NAME = ['資工', '外文', '工管', '機械', '生傳', '政治', '法律']
INSTITUTES_ID = [
	40, # 德田館 
	22, # 文學院 
	0,  # 管一 
	32, # 工綜
	6,  # BICD
	48, # 社科院
	49  # 霖澤館
]

RESTAURANTS_ID = [
	25, # 活大
	30, # 小福
	2, 	# 小小福
	39, # 女九
	7, 	# 正門
	26, # 西門
	50, # 後門
	13, # 側門
	1, 	# 舟山門
	11,	# 長興街門
	54,	# 公館門
	14  # 大一女
]

CLASS_START_TIME = ['8:10', '9:10', '10:20', '11:20', '12:20', '13:20', '14:20', '15:30', '16:30', '17:30']
CLASS_END_TIME = ['9:00', '10:00', '11:10', '12:10', '13:10', '14:10', '15:10', '16:20', '17:20']
SCHEDULE_STATE = ['IDLE', 'INCLASS', 'MOVING']

MOVING_SPEED = 500.0

MAP = mapmodule.Map()

class Schedule:
	def __init__(self):
		self.startPointID = self.getRandomStartPointID()
		self.destPointsID = []
		self.destTimes = []

		self.arrangeSchedue()
		print (self.destPointsID)
		print (self.destTimes)
		self.arrangeRestaurant()

		print (self.destPointsID)
		print (self.destTimes)
		
		self.startTime = Time.getRandomTimeStamp('07:50', Time.addMinutes(self.destTimes[0], -15)) # 7:50～上課前20分鐘
		self.nextDestIdx = 0
		self.numDestPoints = len(self.destPointsID)
		self.endPointID = self.startPointID
		self.endTime = Time.getRandomTimeStamp(Time.addMinutes(self.destTimes[-1], 20), '20:00') # 下課後20分鐘～20:00

	def arrangeSchedue(self): # Arrange Class Schedule
		i = 0
		while i < len(CLASS_START_TIME)-1: # 每次連續上兩節課
			if random.random() >= 0.5:
				destID = self.getRandomDestPointID()
				if destID == 99: # 系館
					destID = random.choice(INSTITUTES_ID)
				self.destPointsID.append(destID)
				self.destTimes.append(CLASS_START_TIME[i])
				i += 1
				if i < len(CLASS_START_TIME):
					self.destPointsID.append(destID)
					self.destTimes.append(CLASS_START_TIME[i])
			i += 1

	def arrangeRestaurant(self): # Arrange Restaraunt for lunch
		i = 0
		while i < len(self.destTimes) and Time.compare(self.destTimes[i], '<', '12:20'):
			i += 1
		# print ("i =",i)
		# print (self.destTimes[i])
		if i >= len(self.destTimes) or self.destTimes[i] != '12:20':
			if i >= len(self.destTimes):
				self.destPointsID.append(random.choice(RESTAURANTS_ID))
				self.destTimes.append('12:20')
			else:
				self.destPointsID = self.destPointsID[:i] + [random.choice(RESTAURANTS_ID)] + self.destPointsID[i:]
				self.destTimes = self.destTimes[:i] + ['12:20'] + self.destTimes[i:]

		elif i+1 >= len(self.destTimes) or self.destTimes[i+1] != '13:20':
			if i+1 >= len(self.destTimes):
				self.destPointsID.append(random.choice(RESTAURANTS_ID))
				self.destTimes.append('13:20')
			else:
				self.destPointsID = self.destPointsID[:i+1] + [random.choice(RESTAURANTS_ID)] + self.destPointsID[i+1:]
				self.destTimes = self.destTimes[:i+1] + ['13:20'] + self.destTimes[i+1:]
		
		elif i-1 < 0 or self.destTimes[i-1] != '11:20':
			if i-1 < 0:
				self.destPointsID = [random.choice(RESTAURANTS_ID)] + self.destPointsID
				self.destTimes = ['11:20'] + self.destTimes
			else:
				self.destPointsID = self.destPointsID[:i] + [random.choice(RESTAURANTS_ID)] + self.destPointsID[i:]
				self.destTimes = self.destTimes[:i] + ['11:20'] + self.destTimes[i:]
	
	def getRandomStartPointID(self):
		return random.choice(START_POINTS_ID)

	def getRandomDestPointID(self):
		return random.choice(BUILDINGS_ID)

	def print(self):
		print ('---------Schedule---------')
		print ('startPointID :', self.startPointID)
		print ('startPointPosition :', MAP.point_list[self.startPointID].position)
		print ('startTime :', self.startTime)
		print ('destPointsID :', self.destPointsID)
		print ('destPointsPosition : ', end='')
		for i in self.destPointsID:
			print (MAP.point_list[i].position, end='')
		print ('destTimes :', self.destTimes)
		print ('nextDestIdx :', self.nextDestIdx)
		print ('numDestPoints :', self.numDestPoints)
		print ('endPointID :', self.endPointID)
		print ('endTime: ', self.endTime)
		print ('--------------------------')


class Student:
	def __init__(self, healthState='HEALTHY'):
		self.gender = self.getRandomGender()
		self.instituteIdx = self.getRandomInstituteIdx()
		self.healthState = healthState
		self.scheduleState = 'IDLE' 
		self.schedule = Schedule()
		self.currentPointID = self.schedule.startPointID
		self.nextPointID = self.findNearestPointID()
		self.currentPosition = MAP.point_list[self.schedule.startPointID].position
		self.currentSpeed = 0.0
		self.currentDirection = (0.0, 0.0)
	
	def getRandomGender(self):
		return 'male' if random.choice([0, 1]) == 0 else 'female'
	
	def getRandomInstituteIdx(self):
		return random.randint(0, len(INSTITUTES_NAME)-1)

	def print(self):
		print ('--------------Student--------------')
		print ('gender :', self.gender)
		print ('institute :', INSTITUTES_ID[self.instituteIdx], INSTITUTES_NAME[self.instituteIdx])
		print ('healthState :', self.healthState)
		print ('scheduleState :', self.scheduleState)
		self.schedule.print()
		print ('currentPointID :', self.currentPointID)
		print ('nextPointID :', self.nextPointID)
		print ('currentPosition :', self.currentPosition)
		print ('currentSpeed :', self.currentSpeed)
		print ('currentDirection :', self.currentDirection)
		print ('-----------------------------------')

	def printPositionInfo(self):
		print ('--------------Student--------------')
		print ('scheduleState :', self.scheduleState)
		print ('currentPointID :', self.currentPointID)
		print ('currentPosition :', self.currentPosition)
		print ('nextPointID :', self.nextPointID)
		print ('currentSpeed :', self.currentSpeed)
		print ('currentDirection :', self.currentDirection)
		print ('-----------------------------------')

	def hasNextClass(self, CURRENT_TIME):
		idx = self.schedule.nextDestIdx
		return idx < self.schedule.numDestPoints and Time.compare(Time.addMinutes(CURRENT_TIME, 15), '==', self.schedule.destTimes[idx])

	def findNearestPointID(self):
		nearestPointID = None
		min_dist = INF
		for pointID in MAP.point_list[self.currentPointID].near_points:
			dist = MAP.point_list[pointID].dis_list[self.schedule.destPointsID[self.schedule.nextDestIdx]]
			if dist < min_dist:
				min_dist = dist
				nearestPointID = pointID

		return nearestPointID

	def move(self):

		left_distance = np.linalg.norm(MAP.point_list[self.nextPointID].position - self.currentPosition)
		if np.linalg.norm(self.currentSpeed * self.currentDirection) < left_distance: # 還沒走到下一個點
			self.currentPosition += self.currentSpeed * self.currentDirection

		elif self.nextPointID == self.schedule.destPointsID[self.schedule.nextDestIdx]: # 到教室了
			
			self.currentPosition = MAP.point_list[self.nextPointID].position
			self.schedule.nextDestIdx += 1
			self.currentPointID = self.nextPointID
			assert (self.currentPointID == self.schedule.destPointsID[self.schedule.nextDestIdx])

		else: # 走超過下個點 -> 轉彎
			print ("TURN~~~~~~~~~~~~~~~~~~~")
			left_distance -= np.linalg.norm(self.currentSpeed * self.currentDirection)
			self.currentPosition = MAP.point_list[self.nextPointID].position 
			self.currentPointID = self.nextPointID
			self.nextPointID = self.findNearestPointID()
			# print ("nextPointID =====", self.nextPointID)
			
			D = MAP.point_list[self.nextPointID].position - self.currentPosition
			self.currentDirection = D / np.linalg.norm(D)
			deltaDist = self.currentDirection * self.currentSpeed
			self.currentPosition +=  deltaDist * (left_distance / np.linalg.norm(deltaDist))
			#exit(0)


	def Action(self, CURRENT_TIME):

		if self.scheduleState == 'IDLE' and self.hasNextClass(CURRENT_TIME): # 該上課了
			self.scheduleState = 'MOVING'
			self.currentSpeed = MOVING_SPEED

		if CURRENT_TIME in CLASS_END_TIME: # 下課了
			if self.scheduleState == 'INCLASS':
				if self.hasNextClass(CURRENT_TIME): # 下節有課
					idx = self.schedule.nextDestIdx
					if self.schedule.destPoints[idx] != self.schedule.destPoints[idx-1]: # 下節課不同教室
						self.currentPosition = MAP.point_list[self.currentPointID].position
						self.scheduleState = 'MOVING'
						self.currentSpeed = MOVING_SPEED

						if self.healthState == 'INFECT':
							MAP.point_list[self.currentPointID].infect_prob -= INFECT_PROB

				else: # 下節沒課
					self.currentPosition = MAP.point_list[self.currentPointID].position
					self.scheduleState = 'IDLE'

					if self.healthState == 'INFECT':
							MAP.point_list[self.currentPointID].infect_prob -= INFECT_PROB

		if self.scheduleState == 'MOVING':

			if self.currentPointID != -1:
				nextPointID = self.findNearestPointID()
				D = MAP.point_list[nextPointID].position - self.currentPosition
				self.currentDirection = D / np.linalg.norm(D)
				self.currentPointID = -1

			self.move()

			if (self.currentPosition == MAP.point_list[self.schedule.destPointsID[self.schedule.nextDestIdx]].position).any(): # 到教室了
				print ("Reach the classroom!!")
				self.scheduleState = 'INCLASS'
				self.currentSpeed = 0
				self.currentDirection = (0, 0)
				self.schedule.nextDestIdx += 1

				if self.healthState == 'INFECTED':
					MAP.point_list[self.currentPointID].infect_prob += INFECT_PROB

		elif self.scheduleState == 'INCLASS':
			
			infect_prob = MAP.point_list[self.currentPointID].infect_prob
			if infect_prob > 0 and self.healthState == 'HEALTHY':

				if random.random() <= infect_prob:
					self.healthState = 'INFECTED' # !!!!!!!
					MAP.point_list[self.currentPointID].infect_prob += INFECT_PROB

		


if __name__ == '__main__':
	
	student = Student()
	while Time.compare(student.schedule.destTimes[0], '>=', '09:10'):
		student = Student()
	student.print()

	CURRENT_TIME = '07:50'
	while Time.compare(CURRENT_TIME, '<=', '09:00'):
		print ("CURRENT_TIME :", CURRENT_TIME)
		student.Action(CURRENT_TIME)
		student.printPositionInfo()
		CURRENT_TIME = Time.addMinutes(CURRENT_TIME, 1)





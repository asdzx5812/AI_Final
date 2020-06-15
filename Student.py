import random
import mapmodule
import numpy as np
from Time import Time

INF = 9999999999999999999

HEALTH_STATES = ['HEALTHY', 'INFECTED']
INFECT_PROB = 1.70834e-4 #0.0205 / 120 (1 /min)

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
		# print (self.destPointsID)
		# print (self.destTimes)
		self.arrangeRestaurant()

		# print (self.destPointsID)
		# print (self.destTimes)
		
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
		print ('destPoints :', self.destPointsID)
		for i in self.destPointsID:
			print (MAP.point_list[i].name, end=' ')
		print ("")
		print ('destPointsPosition : ', end='')
		for i in self.destPointsID:
			print (MAP.point_list[i].position, end='')
		print ("")
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
		self.currentDirection = np.array([0.0, 0.0])
	
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
		print ('currentPoint :', self.currentPointID, MAP.point_list[self.currentPointID].name)
		print ('nextPoint :', self.nextPointID, MAP.point_list[self.nextPointID].name)
		print ('currentPosition :', self.currentPosition)
		print ('currentSpeed :', self.currentSpeed)
		print ('currentDirection :', self.currentDirection)
		print ('-----------------------------------')

	def printPositionInfo(self):
		print ('--------------Student--------------')
		print ('scheduleState :', self.scheduleState)
		print ('currentPoint :', self.currentPointID, MAP.point_list[self.currentPointID].name)
		print ('currentPosition :', self.currentPosition)
		print ('nextPoint :', self.nextPointID, MAP.point_list[self.nextPointID].name)
		print ('nestDest : [', self.schedule.nextDestIdx, ']', MAP.point_list[self.schedule.destPointsID[self.schedule.nextDestIdx]].name)
		print ('currentSpeed :', self.currentSpeed)
		print ('currentDirection :', self.currentDirection)
		print ('-----------------------------------')

	def hasNextClass(self, CURRENT_TIME):
		idx = self.schedule.nextDestIdx
		return idx < self.schedule.numDestPoints and Time.compare(Time.addMinutes(CURRENT_TIME, 20), '>=', self.schedule.destTimes[idx])

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

		delta_distance = np.linalg.norm(self.currentSpeed * self.currentDirection)
	
		while delta_distance > 0:
			print ('current Point:', self.currentPointID, self.currentPosition, 'next point:',  self.nextPointID, MAP.point_list[self.nextPointID].position)
			print ("cur_Dir :", self.currentDirection, 'vs', (MAP.point_list[self.nextPointID].position - self.currentPosition) / np.linalg.norm(MAP.point_list[self.nextPointID].position - self.currentPosition))
				
			left_distance_to_next_point = np.linalg.norm(MAP.point_list[self.nextPointID].position - self.currentPosition)
			# print ("id :", self.currentPointID, MAP.point_list[self.currentPointID].name, '->', self.nextPointID,  MAP.point_list[self.nextPointID].name)
			print ("dis =", delta_distance, left_distance_to_next_point)

			if delta_distance >= left_distance_to_next_point: 
				delta_distance -= left_distance_to_next_point

				self.currentPointID = self.nextPointID
				self.currentPosition = MAP.point_list[self.currentPointID].position
				self.nextPointID = self.findNearestPointID()

				#print ("id ~ ", self.currentPointID, MAP.point_list[self.currentPointID].name, '->', self.nextPointID,  MAP.point_list[self.nextPointID].name)
				self.currentDirection = MAP.point_list[self.currentPointID].unit_vec[self.nextPointID]

				#print ("!!!!!!", self.schedule.nextDestIdx, MAP.point_list[self.schedule.destPointsID[self.schedule.nextDestIdx]].name)
				if self.currentPointID == self.schedule.destPointsID[self.schedule.nextDestIdx]: # 到教室了
					print ("Reach the point!!")
					#self.printPositionInfo()
					break
				else:
					print ("Turn to", self.currentPointID, MAP.point_list[self.currentPointID].name)
			
			else: # delta_distance < left_distance_to_next_point
				assert ((self.currentDirection == (MAP.point_list[self.nextPointID].position - self.currentPosition) / np.linalg.norm(MAP.point_list[self.nextPointID].position - self.currentPosition)).all())
				self.currentPointID = -1
				self.currentPosition += self.currentDirection * delta_distance
				break
		self.printPositionInfo()

	def Action(self, CURRENT_TIME):

		if self.scheduleState == 'IDLE':
			if self.hasNextClass(CURRENT_TIME): # 該上課了
				self.scheduleState = 'MOVING'
				self.nextPointID = self.findNearestPointID()
				self.currentSpeed = MOVING_SPEED
				self.currentDirection = MAP.point_list[self.currentPointID].unit_vec[self.nextPointID]
			else:
				pass

		elif self.scheduleState == 'MOVING':

			self.move()

			if self.currentPointID == self.schedule.destPointsID[self.schedule.nextDestIdx]: # 到教室了
				print ("Reach the classroom!! --", CURRENT_TIME)
				#print (MAP.point_list[self.schedule.destPointsID[self.schedule.nextDestIdx]].position)
				self.scheduleState = 'INCLASS'
				self.currentSpeed = 0
				self.currentDirection = np.array([0.0, 0.0])
				self.schedule.nextDestIdx += 1

				print ('-->')
				self.printPositionInfo()

				if self.healthState == 'INFECTED':
					MAP.point_list[self.currentPointID].infect_prob += INFECT_PROB

		elif self.scheduleState == 'INCLASS':

			if CURRENT_TIME in CLASS_END_TIME: # 下課了
				print ("Class ends --", CURRENT_TIME)
			
				if self.hasNextClass(CURRENT_TIME): # 下節有課
					print ("I have next class :", self.schedule.nextDestIdx, MAP.point_list[self.schedule.destPointsID[self.schedule.nextDestIdx]].name)
					idx = self.schedule.nextDestIdx
					if self.schedule.destPointsID[idx] != self.schedule.destPointsID[idx-1]: # 下節課不同教室
						self.currentPosition = MAP.point_list[self.currentPointID].position
						self.scheduleState = 'MOVING'
						self.nextPointID = self.findNearestPointID()
						self.currentSpeed = MOVING_SPEED
						self.currentDirection = MAP.point_list[self.currentPointID].unit_vec[self.nextPointID]

						if self.healthState == 'INFECT':
							MAP.point_list[self.currentPointID].infect_prob -= INFECT_PROB

					else: # 下節同教室
						self.schedule.nextDestIdx += 1

				else: # 下節沒課
					self.currentPosition = MAP.point_list[self.currentPointID].position
					self.scheduleState = 'IDLE'

					if self.healthState == 'INFECT':
						MAP.point_list[self.currentPointID].infect_prob -= INFECT_PROB

			else:

				infect_prob = MAP.point_list[self.currentPointID].infect_prob
				if infect_prob > 0 and self.healthState == 'HEALTHY':
					if random.random() <= infect_prob:
						self.healthState = 'INFECTED'
						MAP.point_list[self.currentPointID].infect_prob += INFECT_PROB




if __name__ == '__main__':
	
	student = Student()
	while Time.compare(student.schedule.destTimes[0], '>=', '09:10'):
		student = Student()
	student.print()

	last_state = 'AAA'
	CURRENT_TIME = '07:50'
	while Time.compare(CURRENT_TIME, '<=', '12:00'):
		print ('===================================================================', CURRENT_TIME)
		student.Action(CURRENT_TIME)
		if student.currentPosition[0] < 0 or student.currentPosition[1] < 0:
			print (student.currentPosition)
		if student.scheduleState != last_state:
			print ("CURRENT_TIME :", CURRENT_TIME)
			student.printPositionInfo()
		last_state = student.scheduleState
		CURRENT_TIME = Time.addMinutes(CURRENT_TIME, 1)





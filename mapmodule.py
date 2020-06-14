import folium
import numpy
import matplotlib.pyplot as plt
from math import radians, cos, sin, asin, sqrt
class Point():
    def __init__(self, name, position, is_building, near_points, dis_list, building_position, offset, gcor_position, gcor_building_position, gcor_offset):
        self.name = name
        self.position = position
        self.is_building = is_building
        self.near_points = near_points
        self.dis_list = dis_list
        self.building_position = building_position
        self.offset = offset
        self.infect_prob = 0
        self.gcor_position = gcor_position
        self.gcor_building_position = gcor_building_position
        self.gcor_offset = gcor_offset

## count the distance between two positions by longitude and lattitude
def haversine(i,j,LOCATIONS):
    lon1 = LOCATIONS[i][1]
    lat1 = LOCATIONS[i][0]
    lon2 = LOCATIONS[j][1]
    lat2 = LOCATIONS[j][0]
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine公式
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # the radius of earth (km)
    return c * r * 1000

def Floyd_Warshall(distance_list,LOCATIONS):
    for i in range(0,len(LOCATIONS)):
        distance_list[i][i] = 0
    for k in range(0,len(LOCATIONS)):     # 嘗試每一個中繼點
        for i in range(0,len(LOCATIONS)): # 計算每一個i點與每一個j點
            for j in range(0,len(LOCATIONS)):
                if (distance_list[i][k] + distance_list[k][j] < distance_list[i][j]):
                    distance_list[i][j] = distance_list[i][k] + distance_list[k][j]
class Map():
    def __init__(self):
        self.point_list = []
        BUILDINGS = ['德田館', '文學院', '管一', 
             '工綜', 'BICD', '社科院',
             '霖澤館', '新生', '博雅', 
             '普通', '共同', '新體', 
             '女九', '男六','大一女', 
             '活大', '小福', '小小福'] #BICD生傳系館
        
        BUILDINGS_LOCATION = numpy.array([[10500,11300], [4850,9500], [6200,4000],
               [9200,10700], [5800,6950], [11200,13000],
               [13000,12800], [6850,11650], [4500,10628],
               [4700,10128], [5600,6600], [2900,14050],
               [7850,11550], [14700,8200], [2400,5850],
               [8700,9500], [5500,10128], [5200,6400]
              ])
        BUILDINGS_LOCATION = BUILDINGS_LOCATION.astype(float)
        BUILDINGS_OFFSET = numpy.array([[200,300], [800,200], [600,400],
              [700,300], [300,300], [700,300],
              [300,400], [300,300], [400,200],
              [500,200], [200,150], [600,500],     
              [300,150], [500,400], [250,250],
              [300,500], [150,200], [100,100]
             ])
        BUILDINGS_OFFSET = BUILDINGS_OFFSET.astype(float)
        LOCATIONS = numpy.array([[6850,4600], [3300,4900], [5350,6000], [5600,6150], [6100,6400],
            [8800,7500], [12700,9100], [14400,7800], [10200,5700], [2800,6100],
            [6250,6600], [6250,6950], [1800,8550], [2500,8250], [3850,8250],
            [5750,8250], [6250,8250], [7350,8250], [8250,8250], [8700,8250],
            [2500,8750], [3850,8750], [4850,9050], [5750,8750], [7350,8750], 
            [8700,8750], [1500,9850], [2500,9850], [3850,9850], [4700,9850],
            [5500,9850], [7350,9850], [9200,10050], [10200,10050], [12350,10000],
            [3850,10628], [10200,10700], [12350,10700], [7350,11300], [7850,11300],
            [10200,11300], [7350,11650], [10200,11800], [12350,11800], [7350,12500],
            [10200,12500], [7350,13000], [7850,13000], [10200,13000], [12350,12800],
            [12350,13400], [3850,13500], [7850,13500], [3850,14050], [1600,6200],
            [3850,14700]
            ])
        LOCATIONS = LOCATIONS.astype(float) 
        BUILDINGS_gcor_LOCATION = numpy.array([[25.019462, 121.541579], [25.017959, 121.536782], [25.0139, 121.5380],
                      [25.018944, 121.5405067], [25.016219, 121.537929], [25.020734, 121.542360],
                      [25.020576, 121.543630], [25.019704, 121.538500], [25.018924, 121.536640],
                      [25.018559, 121.536701], [25.015844, 121.537841], [25.021705, 121.535289],
                      [25.019554, 121.539472], [25.016810, 121.545216], [25.015297, 121.534613],
                      [25.018060, 121.540098], [25.018560, 121.537405], [25.015412, 121.537199]
                     ])
        BUILDINGS_gcor_OFFSET = numpy.array([[0.0002, 0.0002], [0.0002, 0.0005], [0.0002, 0.0002],
                    [0.0002, 0.0005], [0.0001, 0.0001], [0.0001, 0.0007],
                    [0.0002, 0.0001], [0.0001, 0.0002], [0.00012,0.0004],
                    [0.00013, 0.0004], [0.0001, 0.00015], [0.0003, 0.0004],
                    [0.00013, 0.00017], [0.0002, 0.0003], [0.0002, 0.00028],
                    [0.00026, 0.0003], [0.00016,0.0002], [0.0001, 0.0002]
                   ])
        
        POINTS = ['管一', '舟山門', '小小福', '小木屋', '舟山路轉折點1', # 0~4
          '舟山路轉折點2', '長興街門', '男六', '側門', '大一女', # 5~9
          '共同', 'BICD', '正門', '椰林轉折點1', '椰林轉折點2', # 10~14
          '椰林轉折點3', '椰林轉折點4', '椰林轉折點5', '椰林轉折點6', '椰林轉折點7', #15~19
          '椰林轉折點8', '椰林轉折點9', '文學院', '椰林轉折點10', '椰林轉折點11', #20~24
          '活大', '西門', '蒲葵轉折點1', '蒲葵轉折點2', '普通', #25~29
          '小福', '小椰林轉折點1', '工綜', '水杉道轉折點1', '鄭江樓轉折點1', #30~34
          '博雅', '檀香道轉折點1', '鄭江樓轉折點2', '小椰林轉折點2', '女九', #35~39
          '德田館', '新生', '檀香道轉折點2', '後門路轉折點', '小椰林轉折點3', #40~44
          '檀香道轉折點3', '小椰林轉折點4', '思亮館轉折點1', '社科院', '霖澤館', #45~49
          '後門', '新體轉折點', '思亮館轉折點2', '新體', '公館門',#50~54
          '新體門' #55
         ]
        
        gcor_LOCATIONS = numpy.array([[25.0142, 121.5385], [25.0146, 121.5355], [25.0153, 121.5373], [25.0154, 121.5376], [25.0156, 121.5381], 
             [25.0165, 121.5402], [25.0178, 121.5435], [25.0166, 121.5451], [25.0150, 121.5414], [25.0153, 121.5349],
             [25.0158, 121.5380], [25.0162, 121.5381], [25.0169, 121.5340], [25.0169, 121.5347], [25.0170, 121.5359],
             [25.0170, 121.5377], [25.0170, 121.5381], [25.0170, 121.5390], [25.0170, 121.5398], [25.0170, 121.5401],
             [25.0174, 121.5347], [25.0175, 121.5359], [25.0176, 121.5368], [25.0175, 121.5377], [25.0175, 121.5390],
             [25.0175, 121.5401], [25.0183, 121.5339], [25.0183, 121.5347], [25.0183, 121.5359], [25.0183, 121.5368],
             [25.0183, 121.5374], [25.0184, 121.5390], [25.0185, 121.5405], [25.0185, 121.5413], [25.0184, 121.5432],
             [25.0189, 121.5359], [25.0190, 121.5413], [25.0190, 121.5433], [25.0193, 121.5389], [25.0193, 121.5394],
             [25.0193, 121.5413], [25.0197, 121.5389], [25.0198, 121.5413], [25.0198, 121.5433], [25.0203, 121.5389],
             [25.0202, 121.5412], [25.0207, 121.5389], [25.0207, 121.5392], [25.0208, 121.5412], [25.0205, 121.5434],
             [25.0209, 121.5434], [25.0211, 121.5358], [25.0210, 121.5392], [25.0216, 121.5358], [25.0155, 121.5341],
             [25.0221, 121.5358]
            ])
        
        near_list = [[3], [2,9], [1,3], [0,2,4], [3,5,10], #0~4
             [4,6,8,18], [5,7,34], [6], [5], [1,54], #5-9
             [4,11], [10,16], [13], [12,14,20], [13,15,21], #10-14
             [14,16,23], [11,15,17], [16,18,24], [5,17,19], [18,25], #15-19
             [13,21,27], [14,20,22,28], [21,23], [15,22,24,30], [17,23,25,31], #20-24
             [19,24,32], [27], [20,26,28], [21,27,29,35], [28,30], #25-29
             [23,29,31], [24,30,32,38], [25,31,33], [32,34,36], [6,33,37], #30-34
             [28,51], [33,37,40], [34,36,43], [31,39,41], [38,40], #35-39
             [36,39,42], [38,44], [40,43,45], [37,42,49], [41,45,46], #40-44
             [42,44,48], [44,47], [46,52], [45], [43,50], #45-49
             [49], [35,52,53], [47,51], [51,55], [9],#50-53
             [53]
            ]
                #construct adjacency matrix and count the shortest path
        MAXDIST = 999999999
        distance_list = []
        for i in range(0,len(gcor_LOCATIONS)):
            tmp_list = [MAXDIST]*len(gcor_LOCATIONS)
            for j in near_list[i]:
                tmp_list[j] = haversine(i,j,gcor_LOCATIONS)
            distance_list.append(tmp_list)
        Floyd_Warshall(distance_list,gcor_LOCATIONS)

        #MAP裝所有的點
        #Point代表點(分為建築物前面的點和轉折點兩種)
        #建築物前面的點就代表建築物(裡面多存建築物真正的經緯度和offset(用來取範圍))
        #distance_list維護兩點最近距離
  
        for i in range(0,len(LOCATIONS)):
            is_building = 0
            building_location = [0,0]
            offset = [0,0]
            if POINTS[i] in BUILDINGS:
                is_building = 1
                building_location_index = BUILDINGS.index(POINTS[i])
                building_location = BUILDINGS_LOCATION[building_location_index]
                gcor_building_location = BUILDINGS_gcor_LOCATION[building_location_index]
                offset = BUILDINGS_OFFSET[building_location_index]
                gcor_offset = BUILDINGS_gcor_OFFSET[building_location_index]
            #print(POINTS[i], LOCATIONS[i], is_building, near_list[i], distance_list[i], building_location, offset)
            tmp_point = Point(POINTS[i], LOCATIONS[i], is_building, near_list[i], distance_list[i], building_location, offset, gcor_LOCATIONS[i],gcor_building_location, gcor_offset)
            self.add(tmp_point)
    def add(self,point):
        self.point_list.append(point)

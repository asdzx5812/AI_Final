# 2020AI_Final
- B06705059 資工三 魏任擇
- B06505017 資工二 謝心默
- B06902033 資工三 黃奕鈞

### POINT Class
- POINT代表點
  - **name** : 該點的名字
  - **position** : x,y座標
    - ex: [6000, 4800]
  - **is_building** : 是否為建築物的代表點
    - 1 for building , 0 for no
  - **near_points** : 一個list記錄所有相鄰的點, 用編號(數字)紀錄
  - **dis_list** : 一個list紀錄該點到所有點之間的最短距離
    - dis_list[0] 代表此點到第0點的距離，哪些點分別代表哪些編號可至下面查詢
  - **building_position** : is_building為1的話，此點會記錄代表的建築物的中心位置
    - 一樣使用經緯度
    - is_building 若為 0，此點無值 [0,0]
  - **offset** : 與building_position相似，紀錄代表的建築物的偏移量(x,y座標)
    - 將此值+-中心位置可得範圍
  - **gcor_position** : 經緯度
  - **gcor_building_position** : 建築物經緯度
  - **gcor_offset** : 偏移量(經緯度)
  - **unit_vec** : a dictionary which the unit vector with it's nearly points
```
class Point():
    def __init__(self, name, position, is_building, near_point, dis_list, building_location, offset):
        self.name = name
        self.position = position
        self.is_building = is_building
        self.near_points = near_points
        self.dis_list = dis_list
        self.building_position = building_position
        self.offset = offset

```
   
#### Point 編號
```
 POINTS = ['管一', '舟山門', '小小福', '小木屋', '舟山路轉折點', # 0~4
          '舟山路轉折點', '長興街門', '男六', '側門', '大一女', #10~14
          '共同', 'BICD', '正門', '椰林轉折點', '椰林轉折點', # 5~9
          '椰林轉折點', '椰林轉折點', '椰林轉折點', '椰林轉折點', '椰林轉折點', #15~19
          '椰林轉折點', '椰林轉折點', '文學院', '椰林轉折點', '椰林轉折點', #20~24
          '活大', '西門', '蒲葵轉折點', '蒲葵轉折點', '普通', #25~29
          '小福', '小椰林轉折點', '工綜', '水杉道轉折點', '鄭江樓轉折點', #30~34
          '博雅', '檀香道轉折點', '鄭江樓轉折點', '小椰林轉折點', '女九', #35~39
          '德田館', '新生', '檀香道轉折點', '後門路轉折點', '小椰林轉折點', #40~44
          '檀香道轉折點', '小椰林轉折點', '思亮館轉折點', '社科院', '霖澤館', #45~49
          '後門', '新體轉折點', '思亮館轉折點', '新體', '公館門', #50~54
          '新體門' #55
         ]
```

### MAP Class
Map裡存的是每個點集合起來的list 
```
  class Map():
      def __init__(self):
          self.point_list = []
```        
### 傳染率計算
```
$R_0$ = 傳染率(每次接觸) * 平均每人每日接觸人數 * 世代
$R_0$估計約為3.5(without lockdown)
以個人經驗:平均每日約上2~3門課，每門課有在接觸可能15~20個人(坐在附近)
因此估算平均每人每日接觸50人
而一個世代約為3.4天
(ref:http://www.publichealth.org.tw/upload/files/%E7%AC%AC%E4%B8%89%E5%A0%82%E8%AA%B2%EF%BC%BF%E6%96%B0%E5%86%A0%E8%82%BA%E7%82%8E%E4%B9%8B%E5%82%B3%E6%92%AD%E5%88%86%E6%9E%90(1).pdf)
因此估計傳染率(每次接觸)為3.5/(50*3.4)=0.0205
```

### Position and path in Map
![](https://i.imgur.com/0TM248e.jpg)

### Schedule Class
- Attributes
  - startPointID: 起點編號（到校位置）
  - startTime: 起點時間（到校時間）
  - destPointsID: 上課教室&午餐地點編號
  - destTimes: 上課&午餐時間
  - endPointID: 終點編號（離校位置）
  - endTime: 終點時間（離校時間）
  - nextDestIdx: 下一個目的地（教室/餐廳）的index
  - numDestPoints: len(destPointsID)

- Methods
  - newDayInit(day): 第day天的初始化
  - arrangeSchedule(): 安排課表
  - arrangeRestaurant(): 選擇餐廳與吃飯時間
  - getRandomStartPointID(gender)
  - getRandomDestPointID()
  - print()
  
### Student Class
- Attributes
  - gender: 性別
  - institudeIdx: 科系index
  - healtState: 當前健康狀態，分為'HEALTHY'和'INFECTED'
  - schedule: Schedule()
  - scheduleState: 當前上課狀態，分為'IDLE','MOVING','INCLASS'
  - currentPointID: 當前站在哪個Point上，若在兩點之間移動則為-1
  - nextPointID: 下一個要到的Point，利用findNearestPointID()找到
  - currentPosition: 當前x, y位置
  - currentSpeed: 當前移動速度，目前恆等於MOVING_SPEED
  - currentDirection: 當前移動方向，等於MAP.point_list[currentPointID].unit_vec[nextPointID]
  - visible: 當前是否在校園中

- Methods:
  - getRandomGender()
  - getRandomInstituteIdx()
  - print()
  - printPositionInfo()
  - hasNextClass(CURRENT_TIME): 判斷下一節課上課時間or吃飯時間是否在20分鐘內
  - timeToLeave(CURRENT_TIME): 判斷是否沒課且回家時間在20分鐘內
  - findNearestPointID(day): 根據currentPointID找到下一個離目的地教室/餐廳最近的點
  - move(day): 往目的地移動
  - Action(CURRENT_TIME, day): 每個時間點檢查狀態、進行動作

- Usage:
```
student = Student()

for day in range(5):
    student.newDayInit(day)
    CURRENT_TIME = '07:40'
    while Time.compare(CURRENT_TIME, '<=', '20:00'):
        student.Action(CURRENT_TIME, day)
        if student.visible:
            # show him/her on the map
        else:
            # hide him/her on the map
    CURRENT_TIME = Time.addMinutes(CURRENT_TIME, 1)
```

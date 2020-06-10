# 2020AI_Final
- B06705059 資工三 魏任擇
- B06505017 資工二 謝心默
- B06902033 資工三 黃奕鈞

### POINT Class
- POINT代表點
  - **name** : 該點的名字
  - **position** : 經緯度
    - ex: [21.xxxx, 121.xxxx]
  - **is_building** : 是否為建築物的代表點
    - 1 for building , 0 for no
  - **near_points** : 一個list記錄所有相鄰的點, 用編號(數字)紀錄
  - **dis_list** : 一個list紀錄該點到所有點之間的最短距離
    - dis_list[0] 代表此點到第0點的距離，哪些點分別代表哪些編號可至下面查詢
  - **building_position** : is_building為1的話，此點會記錄代表的建築物的中心位置
    - 一樣使用經緯度
    - is_building 若為 0，此點無值 [0,0]
  - **offset** : 與building_position相似，紀錄代表的建築物的偏移量
    - 將此值+-中心位置可得範圍
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
```

### MAP Class
Map裡存的是每個點集合起來的list 
```
  class Map():
      def __init__(self):
          self.point_list = []
```        

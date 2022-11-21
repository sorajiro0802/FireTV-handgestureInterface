import numpy as np

class gestureDetector:
    def __init__(self, result, required_frame):
        # both hand results
        self.result = result
        self.required_frame = required_frame
        self.hand_node = None
        self.pre_point, self.cur_point = 0, 0
        self.c1 = Counter()
        self.dires = []
        self.direction = None
        
    def detect(self, erapsed_time):
        # 8：人差し指の先端
        finger_direc = self.getPointsDirection(8, erapsed_time)
        isGrub = self.getGrub(0.1)
        return isGrub, finger_direc
    
    def getPointsDirection(self, point_num, erapsed_time):
        # 1 count ≈ 0.035 sec
        if self.c1.cnt > 0:
            self.c1.up()

        if self.c1.cnt == 0:
            # get 0s point
            self.pre_point = np.array( [self.hand_node[point_num].x,
                                        self.hand_node[point_num].y])
            self.c1.up()

        if self.c1.cnt == self.required_frame:
            # get 0.035*frame[s] point
            self.cur_point = np.array( [self.hand_node[point_num].x, 
                                        self.hand_node[point_num].y])  
            P = self.cur_point - self.pre_point
            abs_P = np.linalg.norm(P, ord=2)
            if abs_P < 0.03:
                direc = " "
            else:
                # arccosの値域を拡大する
                if P[1] >= 0: # P_y >= 0
                    angle = -np.arccos(P[0]/abs_P)
                else:
                    angle = np.arccos(P[0]/abs_P)
                angle = angle * 180 / np.pi # convert radian to degree
                
                # judge changed direction
                if 0 <= angle < 45 or -45 <= angle < 0:
                    direc = 'l'
                elif 45 <= angle < 135:
                    direc = 'u'
                elif -135 <= angle < -45:
                    direc = 'd'
                else:
                    direc = 'r'
            self.dires.insert(0, direc) #enqueue
            if len(self.dires) == 2:
                dires_sum = "".join(self.dires)
                if dires_sum == "rr":
                    self.direction = "Right"
                elif dires_sum == "ll":
                    self.direction = "Left"
                elif dires_sum == "uu":
                    self.direction = "Up"
                elif dires_sum == "dd":
                    self.direction = "Down"
                else:
                    self.direction = None
                self.dires.pop()
            self.c1.clear()
            
            # Judging by threshold of acceleration
            ac = abs_P / erapsed_time**2
            if ac > 40 and self.direction:
                return self.direction
            
    def getGrub(self, dist):
        thumb_tip = np.array([self.hand_node[4].x, self.hand_node[4].y, self.hand_node[4].z])
        index_finger_mcp = np.array([self.hand_node[5].x, self.hand_node[5].y, self.hand_node[5].z])
        middle_finger_pip = np.array([self.hand_node[10].x, self.hand_node[10].y, self.hand_node[10].z])
        ring_finger_pip = np.array([self.hand_node[14].x, self.hand_node[14].y, self.hand_node[14].z])
        
        dist4_5 = np.linalg.norm(thumb_tip-index_finger_mcp, ord=2)
        dist4_10 = np.linalg.norm(thumb_tip-middle_finger_pip, ord=2)
        dist4_14 = np.linalg.norm(thumb_tip-ring_finger_pip, ord=2)
        if (dist4_10 or dist4_5 or dist4_14) <= dist:
            return True
        else:
            return False
    
    def updateResults(self, result):
        self.result = result
        self.hand_node = self.result.landmark

class Counter:
    def __init__(self):
        self.cnt = 0

    def up(self):
        self.cnt += 1
    
    def down(self):
        self.cnt -= 1

    def clear(self):
        self.cnt = 0

if __name__=='__main__':
    print(f"hello {__name__}")
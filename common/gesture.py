
import numpy as np

class gestureDetector:
    def __init__(self, result, required_frame):
        # both hand results
        self.result = result
        self.required_frame = required_frame
        self.hand_node = None
        self.gesture = None
        self.c = Counter()
        self.pre_vec = 0
        self.cur_point = 0

    def detect(self):
        # 8：人差し指の先端
        self.pointDirection(8)
    
    def pointDirection(self, point_num):
        # 1 count ≈ 0.035 sec
        if self.c.cnt == 0:
            self.pre_point = np.array( [self.hand_node[point_num].x,
                                        self.hand_node[point_num].y,
                                        self.hand_node[point_num].z])
            self.c.up()
        if self.c.cnt == self.required_frame:
            self.cur_point = np.array( [self.hand_node[point_num].x, 
                                        self.hand_node[point_num].y, 
                                        self.hand_node[point_num].z])  
            self.c.clear()  
        if self.c.cnt > 0:
            self.c.up()
        
        P = self.cur_point - self.pre_point
        abs_P = np.linalg.norm(P, ord=2)
        # print(f'{abs_P=}')
        
        # arccosの値域を拡大する
        if P[1] >= 0: # P_y >= 0
            angle = -np.arccos(P[0]/abs_P)
        else:
            angle = np.arccos(P[0]/abs_P)
        angle = angle * 180 / np.pi # convert raian to degree
        print(f'{angle=}')

        '''
        if  -45 < angle <= 45:
            res = "Right"
        elif -135 < angle <= 135:
            res = "Left"
        # elif -135 < angle 
        '''

    def grub(self, dist):
        thumb_tip = self.hand_node[4]
        index_finger_mcp = self.hand_node[5]
        middle_finger_pip = self.hand_node[10]
        ring_finger_pip = self.hand_node[14]
        
        dist4_5 = np.sqrt(
            (thumb_tip.x-index_finger_mcp.x)**2 +
            (thumb_tip.y-index_finger_mcp.y)**2 +
            (thumb_tip.z-index_finger_mcp.z)**2
        )
        dist4_10 = np.sqrt(
            (thumb_tip.x-middle_finger_pip.x)**2 +
            (thumb_tip.y-middle_finger_pip.y)**2 +
            (thumb_tip.z-middle_finger_pip.z)**2
        )
        dist4_14 = np.sqrt(
            (thumb_tip.x-ring_finger_pip.x)**2 +
            (thumb_tip.y-ring_finger_pip.y)**2 +
            (thumb_tip.z-ring_finger_pip.z)**2
        )
        if (dist4_10 or dist4_5 or dist4_14) <= dist:
            return True
        else:
            return False
    
    def updateResults(self, result):
        self.result = result
        self.hand_node = self.result.landmark
        
    # test stub
    def finger1(self):
        print(self.result.landmark[8])

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
    pass

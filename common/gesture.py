from multiprocessing import Process
import time

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
        # if self.grub(0.1):
        #     print("ぎゅっっ")
        # else:
        #     print("っっぱ")
        # 8：人差し指の先端
        self.pointDirection(8)
    
    def pointDirection(self, point_num):
        if self.c.cnt == 0:
            self.pre_point = np.array([self.hand_node[point_num].x, self.hand_node[point_num].y, self.hand_node[point_num].z])
            self.c.up()
        if self.c.cnt == 10:
            self.cur_point = np.array([self.hand_node[point_num].x, self.hand_node[point_num].y, self.hand_node[point_num].z])  
            self.c.clear()  
        if self.c.cnt >= 1:
            self.c.up()
        try:
            p = self.cur_point - self.pre_point
            abs_p = np.linalg.norm(p, ord=2)
            print(abs_p)
        except:
            pass
        

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

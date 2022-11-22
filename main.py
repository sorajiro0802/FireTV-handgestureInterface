import sys
import time

import cv2
from gestureInterface import gestureInterface
from common.fireTV import FTVController


start_time = time.time()
# for camera input
cap = cv2.VideoCapture(0)
# # for FireTV Connection
# fc = FTVController(ip="192.168.0.20")
# # stop if cann not connect
# if not fc.connect()==0:
#     sys.exit()

command_map = { "Up":{
                    "lhand":{"grub":None, "dire":None},
                    "rhand":{"grub":True, "dire":"Up"}},
                "Down":{
                    "lhand":{"grub":None, "dire":None},
                    "rhand":{"grub":True, "dire":"Down"}},
                "Left":{
                    "lhand":{"grub":None, "dire":None},
                    "rhand":{"grub":True, "dire":"Left"}},
                "Right":{
                    "lhand":{"grub":None, "dire":None},
                    "rhand":{"grub":True, "dire":"Right"}},
                "Select":{
                    "lhand":{"grub":True, "dire":None},
                    "rhand":{"grub":True,  "dire":None}}, 
                "Back":{
                    "lhand":{"grub":None, "dire":None},
                    "rhand":{"grub":False, "dire":"Left"}}
                }
exe_command = []
gi = gestureInterface(cap, command_map)

while True:
    erapsed_time = time.time() - start_time
    ans = gi.Interface()
    exe_command.append(ans)
    # send command
    # fc.command(exe_command)
    
    

if __name__=="__name__":
    pass
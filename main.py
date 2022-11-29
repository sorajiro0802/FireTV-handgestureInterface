import sys

import cv2
from gestureInterface import GestureInterface
from common.fireTV import FTVController

# for camera input
cap = cv2.VideoCapture(0)
# for FireTV Connection
fc = FTVController(ip="192.168.0.20")
# stop if cann not connect
if not fc.connect()==0:
    sys.exit()

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
exe_commands = []
gi = GestureInterface(cap, command_map)

# for stop whileTrue when window closed
isAlive = True
while isAlive:
    ans, isAlive = gi.Interface()
    exe_commands.append(ans)
    # send command
    while exe_commands:
        command = exe_commands.pop(0)
        fc.command(command)


if __name__=="__name__":
    pass
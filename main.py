import sys
import threading

import cv2
from gestureInterface import GestureInterface
from util.fireTV import FTVController


if __name__=="__main__":
    # for camera input
    cap = cv2.VideoCapture(0)
    # for FireTV Connection
    fc = FTVController(ip="192.168.0.20")
    # stop if cann not connect
    if not fc.connect()==0:
        sys.exit()
    # define original gesture
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
            exe_thread = threading.Thread(target=fc.command, args=(command,), daemon=True)
            exe_thread.start()
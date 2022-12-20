import sys
import threading

import cv2
from util.gestureInterface import GestureInterface
from util.fireTV import FTVController
from util.arduino import ArduinoController

if __name__=="__main__":
    # for camera input
    cap = cv2.VideoCapture(0)
    # for FireTV Connection
    # target = FTVController(ip="192.168.0.20")
    target = ArduinoController(port="/dev/cu.usbmodem101")
    
    # stop if cann not connect
    if target.connect() != 0:
        sys.exit()
    # define original gesture
    # command_map = { "Up":{
    #                     "lhand":{"grub":None, "dire":None},
    #                     "rhand":{"grub":True, "dire":"Up"}},
    #                 "Down":{
    #                     "lhand":{"grub":None, "dire":None},
    #                     "rhand":{"grub":True, "dire":"Down"}},
    #                 "Left":{
    #                     "lhand":{"grub":None, "dire":None},
    #                     "rhand":{"grub":True, "dire":"Left"}},
    #                 "Right":{
    #                     "lhand":{"grub":None, "dire":None},
    #                     "rhand":{"grub":True, "dire":"Right"}},
    #                 "Select":{
    #                     "lhand":{"grub":True, "dire":None},
    #                     "rhand":{"grub":True,  "dire":None}}, 
    #                 "Back":{
    #                     "lhand":{"grub":None, "dire":None},
    #                     "rhand":{"grub":False, "dire":"Left"}},
    #                 "Home":{
    #                     "lhand":{"grub":False, "dire":"Up"},
    #                     "rhand":{"grub":False, "dire":"Up"}},
    #                 "StartStop":{
    #                     "lhand":{"grub":True, "dire":None},
    #                     "rhand":{"grub":None, "dire":None}}
    #                 }
    command_map = { "RGrub":{
                        "lhand":{"grub":None, "dire":None},
                        "rhand":{"grub":True, "dire":None}},
                    "LGrub":{
                        "lhand":{"grub":True, "dire":None},
                        "rhand":{"grub":None, "dire":None}}
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
            # for not to delay capturing when command send
            exe_thread = threading.Thread(target=target.command, args=(command,), daemon=True)
            exe_thread.start()
    
    target.kill()
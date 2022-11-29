import sys
import threading

import cv2
from gestureInterface import GestureInterface
from util.fireTV import FTVController

class FTVController:
    def __init__(self, ip):
        self.ip = ip
    def connect(self):
        return 0
    def command(self, command):
        print(command)

if __name__=="__main__":
    # for camera input
    cap = cv2.VideoCapture(0)
    # for FireTV Connection
    target = FTVController(ip="192.168.0.20")
    # stop if cann not connect
    if not target.connect()==0:
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
                        "rhand":{"grub":False, "dire":"Left"}},
                    "Home":{
                        "lhand":{"grub":False, "dire":"Up"},
                        "rhand":{"grub":False, "dire":"Up"}
                    }
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
            exe_thread = threading.Thread(target=target.command, args=(command,), daemon=True)
            exe_thread.start()
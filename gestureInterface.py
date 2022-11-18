import time
import sys

from numpy import floor
import cv2
import mediapipe as mp
from common.gesture import gestureDetector
from common.fireTV import FTVController


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic
mp_hands = mp.solutions.hands

min_detection_frame = 3
detectorR = gestureDetector(result=None, required_frame=min_detection_frame)
detectorL = gestureDetector(result=None, required_frame=min_detection_frame)

# # For fireTV connection
# fc = FTVController(ip='192.168.0.20')
# # stop if can not connect
# if not fc.connect() == 0:
#     sys.exit()

# For webcam input:
cap = cv2.VideoCapture(0)

command_map = { "Up":{
                    "lhand":{"grub":True, "dire":None},
                    "rhand":{"grub":True, "dire":"Up"}},
                "Down":{
                    "lhand":{"grub":True, "dire":None},
                    "rhand":{"grub":True, "dire":"Down"}},
                "Left":{
                    "lhand":{"grub":True, "dire":None},
                    "rhand":{"grub":True, "dire":"Left"}},
                "Right":{
                    "lhand":{"grub":True, "dire":None},
                    "rhand":{"grub":True, "dire":"Right"}},
                "Select":{
                    "lhand":{"grub":False, "dire":None},
                    "rhand":{"grub":True,  "dire":None}}, 
                "Back":{
                    "lhand":{"grub":False, "dire":None},
                    "rhand":{"grub":False, "dire":"Left"}}
                }

with mp_holistic.Holistic(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        # for FPS
        tick = cv2.getTickCount()
        command_flag = {"lhand":{"grub": None, "dire": None},
                        "rhand":{"grub": None, "dire": None}}
        command_flag_tmp = command_flag.copy()
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue
        start_time = time.time()
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # display FPS
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - tick)
        cv2.putText(image, f"{floor(fps)}fps", (60, 60), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2, cv2.LINE_AA)
        erapsed_time = (cv2.getTickCount() - tick) / cv2.getTickFrequency()

        if results.left_hand_landmarks:
            # draw LeftHand landmarks
            mp_drawing.draw_landmarks(  image,
                                        results.left_hand_landmarks,
                                        mp_holistic.HAND_CONNECTIONS,
                                        mp_drawing_styles.get_default_hand_landmarks_style(),
                                        mp_drawing_styles.get_default_hand_connections_style())
            # detect gesture of LeftHand
            detectorL.updateResults(results.left_hand_landmarks)
            grub, dire = detectorL.detect(erapsed_time)
            command_flag["lhand"]["grub"] = grub
            command_flag["lhand"]["dire"] = dire

        if results.right_hand_landmarks:
            # draw RightHand landmarks
            mp_drawing.draw_landmarks(  image,
                                        results.right_hand_landmarks,
                                        mp_holistic.HAND_CONNECTIONS,
                                        mp_drawing_styles.get_default_hand_landmarks_style(),
                                        mp_drawing_styles.get_default_hand_connections_style())
            # detect gesture of RightHand
            detectorR.updateResults(results.right_hand_landmarks)
            grub, dire = detectorR.detect(erapsed_time)
            command_flag["rhand"]["grub"] = grub
            command_flag["rhand"]["dire"] = dire
        print(command_flag)
        for cmk in command_map.keys():
            if command_flag == command_map.get(cmk):
                print(f"{cmk}=")
                # send command
                # fc.command(cmk)
        
        # reset command flag
        command_flag = command_flag_tmp
        # Flip the image horizontally for a selfie-view display.
        #cv2.imshow('FireTV HandGesture Controller', cv2.flip(image, 1))
        # not flip the image
        cv2.imshow('FireTV HandGesture Controller', image)

        # Finish to press Esc
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()
# fc.kill()
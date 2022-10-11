from numpy import floor
import time

import cv2
import mediapipe as mp
from common.gesture import *
from common.fireTV import *
import time

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic
mp_hands = mp.solutions.hands

min_detection_frame = 10
detectorR = gestureDetector(result=None, required_frame=min_detection_frame)
detectorL = gestureDetector(result=None, required_frame=min_detection_frame)

# For webcam input:
cap = cv2.VideoCapture(0)
start_time = 0

with mp_holistic.Holistic(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
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

        # draw hands
        if results.left_hand_landmarks:
            mp_drawing.draw_landmarks(  image,
                                        results.left_hand_landmarks,
                                        mp_holistic.HAND_CONNECTIONS,
                                        mp_drawing_styles.get_default_hand_landmarks_style(),
                                        mp_drawing_styles.get_default_hand_connections_style())

        if results.right_hand_landmarks:
            mp_drawing.draw_landmarks(  image,
                                        results.right_hand_landmarks,
                                        mp_holistic.HAND_CONNECTIONS,
                                        mp_drawing_styles.get_default_hand_landmarks_style(),
                                        mp_drawing_styles.get_default_hand_connections_style())
            # detect right hand gesture
            detectorR.update(results.right_hand_landmarks)
            detectorR.c.clear
            detectorR.detect()
            # if cnt == 0:
            #     print(f"befor {detectorR.pointDirection(8).x}")
            #     cnt += 1
            # elif cnt >= 0:
            #     print(f"after {detectorR.pointDirection(8).x}")
            #     cnt = 0

        # display FPS
        end_time = time.time()
        erapsed_time = end_time - start_time
        start_time = 0
        cv2.putText(image, f"{floor(1/erapsed_time)}fps", (60, 60), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2, cv2.LINE_AA)
        
        # Flip the image horizontally for a selfie-view display.
        #cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
        # not flip the image
        cv2.imshow('FireTV HandGesture Controller', image)

        # Finish to press Esc
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()

from numpy import floor
import cv2
import mediapipe as mp
from util.gesture import gestureDetector

class GestureInterface:
    def __init__(self, cap, command_map):
        self.cap = cap
        self.command_map = command_map
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_holistic = mp.solutions.holistic

        min_detection_frame = 3
        self.detectorR = gestureDetector(result=None, required_frame=min_detection_frame)
        self.detectorL = gestureDetector(result=None, required_frame=min_detection_frame)
        
        self.pre_gesture_flag = {"lhand":{"grub": None, "dire": None},
                                 "rhand":{"grub": None, "dire": None}}
    
    def __del__(self):
        self.cap_release()

    def Interface(self):
        with self.mp_holistic.Holistic(
            min_detection_confidence=0.1,
            min_tracking_confidence=0.1) as hands:
            while self.cap.isOpened():
                # for FPS
                tick = cv2.getTickCount()
                gesture_flag = {"lhand":{"grub": None, "dire": None},
                                "rhand":{"grub": None, "dire": None}}
                gesture_flag_tmp = gesture_flag.copy()
                success, image = self.cap.read()
                if not success:
                    print("Ignoring empty camera frame.")
                    # If loading a video, use 'break' instead of 'continue'.
                    continue
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
                elapsed_time = (cv2.getTickCount() - tick) / cv2.getTickFrequency()

                if results.left_hand_landmarks:
                    # draw LeftHand landmarks
                    self.mp_drawing.draw_landmarks(  image,
                                                results.left_hand_landmarks,
                                                self.mp_holistic.HAND_CONNECTIONS,
                                                self.mp_drawing_styles.get_default_hand_landmarks_style(),
                                                self.mp_drawing_styles.get_default_hand_connections_style())
                    # detect gesture of LeftHand
                    self.detectorL.updateResults(results.left_hand_landmarks)
                    grub, dire = self.detectorL.detect(elapsed_time)
                    gesture_flag["lhand"]["grub"] = grub
                    gesture_flag["lhand"]["dire"] = dire

                if results.right_hand_landmarks:
                    # draw RightHand landmarks
                    self.mp_drawing.draw_landmarks(  image,
                                                results.right_hand_landmarks,
                                                self.mp_holistic.HAND_CONNECTIONS,
                                                self.mp_drawing_styles.get_default_hand_landmarks_style(),
                                                self.mp_drawing_styles.get_default_hand_connections_style())
                    # detect gesture of RightHand
                    self.detectorR.updateResults(results.right_hand_landmarks)
                    grub, dire = self.detectorR.detect(elapsed_time)
                    gesture_flag["rhand"]["grub"] = grub
                    gesture_flag["rhand"]["dire"] = dire

                # check whether gesture_flag matchs command_map
                for cmk in self.command_map.keys():
                    if (gesture_flag != self.pre_gesture_flag) & (self.pre_gesture_flag != dict(self.command_map[cmk])):
                        if self.command_map[cmk] == gesture_flag:
                            self.pre_gesture_flag = gesture_flag
                            gesture_flag = gesture_flag_tmp
                            print(f"{cmk=}")
                            return cmk, True
                        
                self.pre_gesture_flag = gesture_flag
                # reset gesture flag
                gesture_flag = gesture_flag_tmp
                # Flip the image horizontally for a selfie-view display.
                # cv2.imshow('FireTV HandGesture Controller', cv2.flip(image, 1))
                # not flip the image
                cv2.imshow('FireTV HandGesture Controller', image)
                
                if cv2.waitKey(5) & 0xFF == 27:
                    self.cap.release()
                    break
    
    def cap_release(self):
        self.cap.release()
        

if __name__=="__main__":
    pass
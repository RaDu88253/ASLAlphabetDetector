import os

import mediapipe as mp
import numpy as np
import cv2



BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

opened = False

# Create a hand landmarker instance with the live stream mode:
def print_result(result: HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    # print('hand landmarker result: {}'.format(result))
    if result.hand_landmarks:
        print(len(result.hand_landmarks))
        # print(type(result.hand_landmarks[0][0]))
        # exit(0)
        # global opened
        # print(os.getcwd())
        # if not opened:
        #     try:
        #         with open('D:\\Projects\\ASLAlphabetDetector\\test\\test.py', 'a') as f:
        #             f.write(str(result.hand_landmarks))
        #
        #             print(os.getcwd())
        #             opened = True
        #     except Exception as e:
        #         print(e)
        #         opened = True
    # print(len(result.hand_world_landmarks[0]))



options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path='hand_landmarker.task'),
    running_mode=VisionRunningMode.LIVE_STREAM,
    num_hands=2,
    result_callback=print_result)
with HandLandmarker.create_from_options(options) as landmarker:

    vc = cv2.VideoCapture(0)
    timestamp = 0
    while True:
        image = vc.read()[1]
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
        landmarker.detect_async(image=mp_image, timestamp_ms=timestamp)
        timestamp += 1
        cv2.imshow('image', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            exit()


import os
import time
import mediapipe as mp
import cv2
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
FILE_NAME = "a.txt"
RAW_DATA_FILE_PATH = Path(os.environ['RAW_DATA_FOLDER']) / FILE_NAME
NUMBER_OF_FRAMES = 1000
MAX_BUFFER_LENGTH = 100

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode


# Clear data file before generating new data
with open(RAW_DATA_FILE_PATH, 'w') as f:
    f.write('')


options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path='hand_landmarker.task'),
    running_mode=VisionRunningMode.VIDEO,
    num_hands=2
)
with HandLandmarker.create_from_options(options) as landmarker:

    vc = cv2.VideoCapture(0)
    buffer = []
    cnt = 0
    while True:
        image = vc.read()[1]
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
        timestamp_ms = int(time.time_ns() / 1000)
        result = landmarker.detect_for_video(image=mp_image, timestamp_ms=timestamp_ms)
        cv2.imshow('image', image)

        if result.hand_landmarks:
            try:
                cnt += 1
                frame_data = []
                # with open(data_file_path, 'a') as f:
                for r in result.hand_landmarks[0]:
                    frame_data.append(f"{r.x},{r.y},{r.z}")
                buffer.append(';'.join(frame_data))

            except Exception as e:
                print(e)

        if len(buffer) >= MAX_BUFFER_LENGTH:
            print(len(buffer))
            print(cnt)
            with open(RAW_DATA_FILE_PATH, 'a') as f:
                f.write('\n'.join(buffer) + '\n')
            buffer.clear()
        if (cv2.waitKey(1) & 0xFF == ord('q')) or cnt == NUMBER_OF_FRAMES:
            if NUMBER_OF_FRAMES % MAX_BUFFER_LENGTH != 0:
                with open(RAW_DATA_FILE_PATH, 'a') as f:
                    f.write('\n'.join(buffer) + '\n')
                buffer.clear()
            cv2.destroyAllWindows()
            exit()


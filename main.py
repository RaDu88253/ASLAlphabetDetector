import json
import torch
import numpy as np
import os
import time
import mediapipe as mp
import cv2
from run_model import HandSignRecogniser

# Initialize model

with open("label_map.json", 'r') as f:
    idx_to_label = json.load(f)
    idx_to_label = {int(k): v for k, v in idx_to_label.items()}

device = "cuda" if torch.cuda.is_available() else "cpu"

NUM_CLASSES = len(idx_to_label)

model_path = "models/hand_model_100_samples.pt"

handSignRecogniser = HandSignRecogniser(model_path=model_path, class_names=idx_to_label)

def validate_output(states):
    res = states[0]
    for state in states:
        if state != res:
            return False
    return True

# Initialize mediapipe

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path='models/hand_landmarker.task'),
    running_mode=VisionRunningMode.VIDEO,
    num_hands=2
)
with HandLandmarker.create_from_options(options) as landmarker:

    vc = cv2.VideoCapture(0)
    buffer = []
    validation_states = [None, None, None, None, None, None, None, None]
    previous_state = None
    cnt = 0
    index = 0
    while True:
        image = vc.read()[1]
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
        timestamp_ms = int(time.time_ns() / 1000)
        result = landmarker.detect_for_video(image=mp_image, timestamp_ms=timestamp_ms)
        # cv2.imshow('image', image)

        if result.hand_landmarks:
            try:
                cnt += 1
                index += 1
                index %= len(validation_states)
                frame_data = []
                # with open(data_file_path, 'a') as f:
                for r in result.hand_landmarks[0]:
                    frame_data.append([1 - r.x, 1 - r.y, r.z])
                frame_data = np.array(frame_data, dtype=np.float32)
                frame_data = frame_data - frame_data[0]
                scale = np.linalg.norm(frame_data[9])
                frame_data = np.divide(frame_data, scale)
                input_tensor = torch.tensor(frame_data).unsqueeze(0).to(device)
                output = handSignRecogniser.predict(input_tensor)[0]
                validation_states[index] = output
                # print(validation_states, validate_output(validation_states))
                if validate_output(states=validation_states) and output != 'undefined' and output != previous_state:
                    # print('\b', end='')
                    print(f"{output}", end='')
                    previous_state = output
            except Exception as e:
                print(e)

        # if len(buffer) >= MAX_BUFFER_LENGTH:
        #     print(len(buffer))
        #     print(cnt)
        #     with open(RAW_DATA_FILE_PATH, 'a') as f:
        #         f.write('\n'.join(buffer) + '\n')
        #     buffer.clear()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            exit()


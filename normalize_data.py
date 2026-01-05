import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

FILENAMES = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k',
             'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
             'v', 'w', 'x', 'y']

for name in FILENAMES:
    file_name = f"{name}.txt"
    raw_data_file_path = Path(os.environ['RAW_DATA_FOLDER']) / file_name
    normalized_data_path = Path(os.environ['DATASET_FOLDER']) / file_name

    # Read lines
    with open(raw_data_file_path, 'r') as f:
        lines = f.readlines()

    # Remove trailing ; and newline, split by ';'
    lines = [line.rstrip("\n").split(';') for line in lines]



    # Split each landmark into [x, y, z] and convert to float
    data = []
    for hand in lines:
        hand_landmarks = []
        for landmark in hand:
            x, y, z = landmark.split(',')
            hand_landmarks.append([float(x), float(y), float(z)])

        data.append(hand_landmarks)

    with open(normalized_data_path, 'w') as f:
        f.write('') # clear dataset file before writing

    # # Pick one frame / hand to plot (e.g., frame index 7)
    # frame_index = 7
    # hand_landmarks = data[frame_index]  # list of 21 landmarks

    for hand_landmarks in data:

        # Extract x and y
        x_points = np.array([1 - lm[0] for lm in hand_landmarks])
        y_points = np.array([1 - lm[1] for lm in hand_landmarks])  # flip y for proper image coordinates
        z_points = np.array([lm[2] for lm in hand_landmarks])

        base_x = x_points[0]
        base_y = y_points[0]
        base_z = z_points[0]

        x_points = np.subtract(x_points, base_x)
        y_points = np.subtract(y_points, base_y)
        z_points = np.subtract(z_points, base_z)

        points = np.array([np.array([x, y, z]) for x, y, z in zip(x_points, y_points, z_points)])

        scale = np.linalg.norm(points[9])

        points = np.divide(points, scale)

        # scale_x = np.abs(x_points[9] - x_points[0])
        # scale_y = np.abs(y_points[9] - y_points[0])
        # scale_z = np.abs(z_points[9] - z_points[0])

        # x_points = np.multiply(x_points, scale_x)
        # y_points = np.multiply(y_points, scale_y)
        # y_points = np.multiply(y_points, scale_z)

        with open(normalized_data_path, 'a') as f:
            entry = []
            for x, y, z in points:
                entry.append(str(x) + ',' + str(y) + ',' + str(z))
            f.write(";".join(entry))
            f.write('\n')




# print(points)
# plt.scatter(points[:, 0], points[:, 1])
# plt.scatter(points[0][0], points[0][1], c='red')
# plt.show()

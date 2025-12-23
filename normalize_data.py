import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

file_name = "a.txt"
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

for entry in data:
    with open(normalized_data_path, 'a') as f:
        for landmark in entry:
            s = str(landmark[0]) + ',' + str(landmark[1]) + ";"
            f.write(s)
        f.write('\n')
        pass

# Pick one frame / hand to plot (e.g., frame index 7)
frame_index = 7
hand_landmarks = data[frame_index]  # list of 21 landmarks

# Extract x and y
xpoints = np.array([1 - lm[0] for lm in hand_landmarks])
ypoints = np.array([1 - lm[1] for lm in hand_landmarks])  # flip y for proper image coordinates

basex = xpoints[0]
basey = ypoints[0]

xpoints = np.subtract(xpoints, basex)
ypoints = np.subtract(ypoints, basey)

max_x = 1 / np.max(xpoints)
max_y = 1 / np.max(ypoints)

xpoints = np.multiply(xpoints, max_x)
ypoints = np.multiply(ypoints, max_y)

# plt.scatter(xpoints, ypoints)
# plt.scatter(xpoints[0], ypoints[0], c='red')
# plt.show()

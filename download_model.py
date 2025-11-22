import requests

url = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task"

with requests.get(url, stream=True) as r:
    r.raise_for_status()
    with open("hand_landmarker.task", "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

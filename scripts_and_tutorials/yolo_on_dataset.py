import fiftyone as fo
import fiftyone.zoo as foz
from fiftyone import ViewField as F
import dataset_wrangling_code.get_boat_dataset as get_boat_dataset

import numpy as np
import os
# from tqdm import tqdm
from ultralytics import YOLO


from ultralytics import YOLO

detection_model = YOLO("yolov8n.pt")
# seg_model = YOLO("yolov8n-seg.pt")

# results = detection_model("https://ultralytics.com/images/bus.jpg")

dataset = get_boat_dataset.get_boats_debug()

model = YOLO("yolov8l.pt")

dataset.apply_model(model,label_field="yolov8l")

session = fo.launch_app(dataset)
session.wait()
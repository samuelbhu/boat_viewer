from ultralytics import YOLO
import os



# Load a COCO-pretrained YOLOv8n model


def run_debug_train():
    model = YOLO("yolov8n.pt")

    directory = "/Users/samuel/git/boat_viewer/datasets/open-images-v7/images/train"
    counter = 0
    MAX_IMAGES = 25
    for filename in os.listdir(directory):
        if counter > MAX_IMAGES:
            break
        full_path = os.path.join(directory, filename)
        if os.path.isfile(full_path):
            results = model(full_path)
            for result in results:
                class_ids = result.boxes.cls.cpu().numpy().astype(int)
                class_names = model.names 
                detected_objects = [class_names[c] for c in class_ids]
                unique_objects = list(set(detected_objects))

                print("Objects detected:", unique_objects)
                counter+=1





def validate_model():
    from ultralytics import YOLO

   
    model = YOLO("yolov8n.pt")  # load an official model
    # model = YOLO("path/to/best.pt")  # load a custom model

    # Validate the model
    metrics = model.val()  # no arguments needed, dataset and settings remembered
    metrics.box.map  # map50-95
    metrics.box.map50  # map50
    metrics.box.map75  # map75
    metrics.box.maps  # a list contains map50-95 of each category
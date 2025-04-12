from ultralytics import YOLO


# Load a COCO-pretrained YOLOv8n model


def run_debug_train():
    model = YOLO("yolov8n.pt")
    results = model("/Users/samuel/git/boat_viewer/sample_images/boat_image_example.jpg")
    for result in results:
        class_ids = result.boxes.cls.cpu().numpy().astype(int)
        class_names = model.names 
        detected_objects = [class_names[c] for c in class_ids]
        unique_objects = list(set(detected_objects))

        print("Objects detected:", unique_objects)

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
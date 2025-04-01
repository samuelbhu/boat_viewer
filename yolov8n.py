from ultralytics import YOLO

detection_model = YOLO("yolov8n.pt")

# results = detection_model("boat_image_example.jpg")
def contains(class_search,image):
    results = detection_model(image)
    for result in results:
        labels = [detection_model.names[int(cls)] for cls in result.boxes.cls]
        print(labels)
        if class_search in labels:
            return True
        else:
            return False

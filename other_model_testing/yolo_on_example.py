from ultralytics import YOLO

detection_model = YOLO("yolov8n.pt")

# results = detection_model("boat_image_example.jpg")
results = detection_model(source=1,show=True)
for result in results:
    labels = [detection_model.names[int(cls)] for cls in result.boxes.cls]
    print(labels)


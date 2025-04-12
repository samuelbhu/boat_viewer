
import requests
from PIL import Image
import torch

from transformers import pipeline
# pipe = pipeline("zero-shot-object-detection", model="google/owlv2-large-patch14-ensemble")


# Load model directly
from transformers import AutoProcessor, AutoModelForZeroShotObjectDetection

processor = AutoProcessor.from_pretrained("google/owlv2-large-patch14-ensemble")
model = AutoModelForZeroShotObjectDetection.from_pretrained("google/owlv2-large-patch14-ensemble")


img = "boat_image_example.jpg"
image = Image.open(img)
texts = ["ship", "boat", "mountian"]
inputs = processor(text=texts, images=image, return_tensors="pt")

with torch.no_grad():
  outputs = model(**inputs)

# Target image sizes (height, width) to rescale box predictions [batch_size, 2]
target_sizes = torch.Tensor([image.size[::-1]])
# Convert outputs (bounding boxes and class logits) to Pascal VOC Format (xmin, ymin, xmax, ymax)
results = processor.post_process_object_detection(outputs=outputs, target_sizes=target_sizes, threshold=0.1)
i = 0  # Retrieve predictions for the first image for the corresponding text queries
text = texts[i]
boxes, scores, labels = results[i]["boxes"], results[i]["scores"], results[i]["labels"]
for box, score, label in zip(boxes, scores, labels):
    box = [round(i, 2) for i in box.tolist()]
    print(f"Detected {text[label]} with confidence {round(score.item(), 3)} at location {box}")
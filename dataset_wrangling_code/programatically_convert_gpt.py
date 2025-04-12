import fiftyone as fo
import fiftyone.zoo as foz
import fiftyone.utils.data as foud

# Load just part of Open Images
dataset = foz.load_zoo_dataset(
    "open-images-v7",
    split="test",
    label_types=["detections"],
    max_samples=50,
)

# Convert to COCO format
foud.convert_dataset(
    dataset,
    input_type=fo.types.OpenImagesV7Dataset,
    output_dir="/Users/samuel/fiftyone/open-images-v7-yolo/",
    output_type=fo.types.YOLOv4Dataset,
    # label_field="detections",  # or whatever your label field is
)

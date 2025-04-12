# This file will get boat related images
# initially I plan to grab only a small number of images for debug
import fiftyone as fo
import fiftyone.zoo as foz

def get_boats_debug():
    dataset = foz.load_zoo_dataset(
        "open-images-v7",
        split="validation",
        label_types=["detections"],
        classes = ["Boat", "Ship", "Submarine", "Barge", "Watercraft"],
        max_samples=100,
        seed=51,
        shuffle=True,
        dataset_name="boat_related_100",
    )
    session = fo.launch_app(dataset.view())
    session.wait()
    return dataset

# get_boats_debug()

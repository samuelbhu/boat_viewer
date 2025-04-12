import fiftyone as fo
import fiftyone.zoo as foz
import fiftyone.utils.data as foud

import os
import yaml




yolo_path = "/Users/samuel/git/yolov7" #where the checkout of yolov7 is located
yolo_model = "yolov7.py" # this should be located in the yolo path

sample_dataset = {
    "name":"open-images-v7", 
    "split":"test"
    }




def run_validation():
    # this function simply verifies that the yolo system, yolo model, and chosen dataset are working
    load_dataset()

def view_dataset_type():
    # Load your dataset
    dataset = fo.load_dataset(sample_dataset["name"])
                              
    # Print basic dataset info
    print(dataset)

def view_fiftyone_datasets():
    downloaded_datasets = foz.list_downloaded_zoo_datasets()
    fo.pprint(downloaded_datasets)


def download_open_images_partial():

    dataset = foz.load_zoo_dataset(
        "open-images-v7",        # or another zoo dataset
        split="test",
        label_types=['classifications', 'detections', 'points', 'relationships', 'segmentations'],
        max_samples=10,          # or any size
        dataset_name="my_openimages_mini_subset",  # name to refer back to later
        persistent=True          # important: saves it to disk!

    )

    for sample in dataset:
        print(sample.filepath)

    print(dataset.get_field_schema())
    return dataset

def convert_dataset_to_yolo(dataset):
    foud.convert_dataset(
        # dataset,
        input_dir="/Users/samuel/fiftyone/open-images-v7/test/",
        output_dir="/Users/samuel/datasets/my_openimages_mini_subset_yolo_format_v2",
        input_type=fo.types.OpenImagesV7Dataset,      # or YOLOv4Dataset, etc.
        output_type=fo.types.YOLOv4Dataset,      # or YOLOv4Dataset, etc.
        # label_field="ground_truth",            # update if yours is different
        # split="test",                       # creates 'train/images' and 'train/labels'
    )

def create_yaml_file(dataset):
    export_dir = "/Users/samuel/datasets/my_openimages_mini_subset_yolo_format_v2"
    classes = dataset.default_classes

    data_yaml = {
        "test": os.path.join(export_dir, "test", "images"),
        "nc":len(classes),
        "names":classes,
    }
    yaml_path = os.path.join(export_dir, "data.yaml")
    with open(yaml_path, "w") as f:
        yaml.dump(data_yaml, f)    



def load_dataset():
    # uses 'dataset' variable above with fiftyone
    # and convert to yolo format
    dataset = foz.load_zoo_dataset(
        sample_dataset["name"],
        split=sample_dataset["split"],
        max_samples=1000,
        seed=51,
        shuffle=True,
        label_types=["detections"]
    )
def convert_to_yolo():
    pass

if __name__ == "__main__":
    dataset = download_open_images_partial()
    convert_dataset_to_yolo(dataset)
    create_yaml_file(dataset)
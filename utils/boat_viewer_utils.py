from ultralytics import YOLO
import os
import requests
import time

import warnings

def check_for_boat(model_name,filename,boat_class):
    model = YOLO(model_name)
    # predictions = {}
    results = model(filename,verbose=False)
    for result in results:
        class_ids = result.boxes.cls.cpu().numpy().astype(int)
        predictions = set([int(id) for id in class_ids])
        print(f"predictions:{predictions}")
        if boat_class in predictions:
            return True
        else:
            return False
        # class_names = model.names 
        # detected_objects = [class_names[c] for c in class_ids]
        # if

def get_model_info(name):
    model = YOLO(name)
    return model.info() 



def get_predictions(model_name,dataset_path,max_images,boat_class=None):
    model = YOLO(model_name)
    if boat_class:
        if model.names[boat_class] != "boat":
            raise ValueError(f"ERROR: Boat Class Mismatch on model {model_name}, which dataset was used for training?")
    counter = 0
    total_model_time = 0.0
    predictions = {}
    for filename in sorted(os.listdir(dataset_path)):
        # input(f"filename:{dataset_path}{filename}")
        # if counter % 20 == 0:
        if counter % max(1,int(max_images/10)) == 0: # setting this to 10 percent printout
            print(f'processed: {counter}/{max_images}')

        if counter >= max_images:
            break
        full_path = os.path.join(dataset_path, filename)
        if os.path.isfile(full_path):
            yolo_start = time.time()
            results = model(full_path,verbose=False)
            yolo_end = time.time()
            total_model_time = (yolo_end-yolo_start) + total_model_time
            for result in results:
                class_ids = result.boxes.cls.cpu().numpy().astype(int)
                predictions[filename.split(".")[0]] = set([int(id) for id in class_ids])

                class_names = model.names 
                detected_objects = [class_names[c] for c in class_ids]

                # unique_objects = list(set(detected_objects)) TODO:delete?

                counter+=1
    
    return predictions,total_model_time/counter

def extract_first_column_integers(filename):
    # print(f"filename:{filename}")
    with open(filename, 'r') as file:
        return {int(line.split()[0]) for line in file if line.strip()}


def get_truths(dataset_truths_path,max_images):
    print(f"dataset path: {dataset_truths_path}")
    print(f"max_images: {max_images}")
    counter = 0
    truths = {}
    for filename in sorted(os.listdir(dataset_truths_path)):
        if counter >= max_images:
            break
        full_path = os.path.join(dataset_truths_path, filename)
        if os.path.isfile(full_path):
            class_ids = extract_first_column_integers(full_path)
            truths[filename.split(".")[0]] = class_ids
            counter+=1
    return truths


def compare_and_report(truths,predictions,target_class_id,max_images,brief=False):
    total_images = max_images
    true_images_with_target = 0
    true_positives = 0
    false_negatives = 0
    false_positives = 0
    true_negatives = 0
    true_positives_arr = []
    false_negatives_arr = []
    false_positives_arr = []
    report = {}

    
    for image in truths.keys():
        if target_class_id in truths[image]:
            true_images_with_target +=1
            if target_class_id in predictions[image]:
                true_positives += 1
                if not brief:
                    true_positives_arr.append(image)
            else:
                false_negatives += 1
                if not brief:
                    false_negatives_arr.append(image)
        else: # no boat in truth
            if target_class_id in predictions[image]:
                false_positives +=1
                if not brief:
                    false_positives_arr.append(image)
            else:
                true_negatives +=1

    print(f'{total_images=}')
    print(f'{true_images_with_target=}')
    print(f'{true_positives=}')
    print(f'{false_negatives=}')
    print(f'{false_positives=}')
    print(f'{true_negatives=}')

    report["total_images"] = total_images
    report["true_images_with_target"] = true_images_with_target
    report["true_positives"] = true_positives
    report["false_positives"] = false_positives
    report["true_negatives"] = true_negatives
    report["false_negatives"] = false_negatives
    if not brief:
        report["false_negatives_arr"] = false_negatives_arr
        report["true_positives_arr"] = true_positives_arr
        report["false_positives_arr"] = false_positives_arr

    return report

def get_dataset(dataset_name, fraction,split,split_size):
    import fiftyone as fo
    import fiftyone.zoo as foz

    from ultralytics.utils import LOGGER, SETTINGS, Path, get_ubuntu_version, is_ubuntu
    from ultralytics.utils.checks import check_requirements, check_version

    check_requirements("fiftyone")
    if is_ubuntu() and check_version(get_ubuntu_version(), ">=22.04"):
        # Ubuntu>=22.04 patch https://github.com/voxel51/fiftyone/issues/2961#issuecomment-1666519347
        check_requirements("fiftyone-db-ubuntu2204")

    dataset_name #"open-images-v7"
    fo.config.dataset_zoo_dir = f"datasets/fiftyone/{dataset_name}_{fraction}"
    # fraction = .01  # fraction of full dataset to use
    # LOGGER.warning("WARNING ⚠️ Open Images V7 dataset requires at least **561 GB of free space. Starting download...")
    
    # Load Open Images dataset
    dataset = foz.load_zoo_dataset(
        dataset_name,
        split=split,
        label_types=["detections"],
        max_samples=round(split_size*fraction)
    )

    classes = dataset.default_classes  # all classes
        # classes = dataset.distinct('ground_truth.detections.label')  # only observed classes

    # Export to YOLO format
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning, module="fiftyone.utils.yolo")
        dataset.export(
            export_dir=f"./datasets/yolo/{dataset_name}_{fraction}",
            dataset_type=fo.types.YOLOv5Dataset,
            label_field="ground_truth",
            # split="val" if split == "validation" else split, # trying to remove this if possible
            split = split,
            classes=classes,
            # overwrite=train,
        )
def upload_image(filename):

    url = "WEBSITE URL"
    # Open the image file in binary mode
    with open(filename, "rb") as image_file:
        files = {"image": image_file}
        data = {
            "title": "Boat Detected",
            "description": "Freeland Mutiny Bay Capture"
        }

        response = requests.post(url, files=files, data=data, verify=False)

    # Print response
    print(response.status_code, response.text)
    return response.status_code == 200

def delete_image(filename):
    print("Deleting Images Soon")
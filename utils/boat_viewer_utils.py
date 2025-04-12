from ultralytics import YOLO
import os

# Load a COCO-pretrained YOLOv8n model

# Number of images to check on

def get_predictions(model_name,dataset_path,max_images):
    model = YOLO(model_name)
    counter = 0
    predictions = {}
    for filename in sorted(os.listdir(dataset_path)):

        # if counter % 20 == 0:
        if counter % max(1,int(max_images/10)) == 0: # setting this to 10 percent printout
            print(f'processed: {counter}/{max_images}')

        if counter >= max_images:
            break
        full_path = os.path.join(dataset_path, filename)
        if os.path.isfile(full_path):
            results = model(full_path,verbose=False)
            for result in results:
                class_ids = result.boxes.cls.cpu().numpy().astype(int)
                predictions[filename.split(".")[0]] = set([int(id) for id in class_ids])

                class_names = model.names 
                detected_objects = [class_names[c] for c in class_ids]

                # unique_objects = list(set(detected_objects)) TODO:delete?

                counter+=1
    return predictions

def extract_first_column_integers(filename):
    # print(f"filename:{filename}")
    with open(filename, 'r') as file:
        return {int(line.split()[0]) for line in file if line.strip()}


def get_truths(dataset_path,max_images):
    print(f"dataset path: {dataset_path}")
    print(f"max_images: {max_images}")
    counter = 0
    truths = {}
    for filename in sorted(os.listdir(dataset_path)):
        if counter >= max_images:
            break
        full_path = os.path.join(dataset_path, filename)
        if os.path.isfile(full_path):
            class_ids = extract_first_column_integers(full_path)
            truths[filename.split(".")[0]] = class_ids
            counter+=1
    return truths


def compare_and_report(truths,predictions,target_class_id,max_images):
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
                true_positives_arr.append(image)
            else:
                false_negatives += 1
                false_negatives_arr.append(image)
        else: # no boat in truth
            if target_class_id in predictions[image]:
                false_positives +=1
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
    report["true_positives_arr"] = true_positives_arr
    report["false_negatives"] = false_negatives
    report["false_negatives_arr"] = false_negatives_arr
    report["false_positives_arr"] = false_positives_arr
    report["true_negatives"] = true_negatives

    return report

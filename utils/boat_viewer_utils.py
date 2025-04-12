from ultralytics import YOLO
import os

# Load a COCO-pretrained YOLOv8n model

# Number of images to check on
MAX_IMAGES = len(os.listdir("/Users/samuel/git/boat_viewer/datasets/open-images-v7/images/train"))

def get_predictions(model_name):
    model = YOLO(model_name)
    directory = "/Users/samuel/git/boat_viewer/datasets/open-images-v7/images/train"
    counter = 0
    # <KEY = FILENAME> <VALUE=SET OF PREDICTED CLASSIDS>
    predictions = {}
    for filename in sorted(os.listdir(directory)):

        if counter % 20 == 0:
            print(f'processed: {counter}/{MAX_IMAGES}')

        if counter >= MAX_IMAGES:
            break
        full_path = os.path.join(directory, filename)
        if os.path.isfile(full_path):
            results = model(full_path,verbose=False)
            for result in results:
                class_ids = result.boxes.cls.cpu().numpy().astype(int)
                # print(f"class ids: {class_ids}")                
                predictions[filename.split(".")[0]] = set([int(id) for id in class_ids])

                class_names = model.names 
                detected_objects = [class_names[c] for c in class_ids]
                unique_objects = list(set(detected_objects))

                # print("Objects detected:", unique_objects)
                counter+=1
    return predictions

def extract_first_column_integers(filename):
    with open(filename, 'r') as file:
        return {int(line.split()[0]) for line in file if line.strip()}


def get_truths(dataset_name):
    directory = "/Users/samuel/git/boat_viewer/datasets/open-images-v7/labels/train"
    counter = 0
    # <KEY = FILENAME> <VALUE=SET OF PREDICTED CLASSIDS>
    truths = {}
    for filename in sorted(os.listdir(directory)):
        if counter >= MAX_IMAGES:
            break
        full_path = os.path.join(directory, filename)
        if os.path.isfile(full_path):
            class_ids = extract_first_column_integers(full_path)
            truths[filename.split(".")[0]] = class_ids
            counter+=1
    return truths


def compare_and_report(truths,predictions,target_class_id):
    total_images = MAX_IMAGES
    true_images_with_target = 0
    true_positives = 0
    false_negatives = 0
    false_positives = 0
    true_negatives = 0
    true_positives_arr = []
    false_negatives_arr = []
    false_positives_arr = []

    
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
    print(f'{true_positives=} | {true_positives_arr}')
    print(f'{false_negatives=} | {false_negatives_arr}')
    print(f'{false_positives=} | {false_positives_arr}')
    print(f'{true_negatives=}')

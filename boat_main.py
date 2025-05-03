#!/opt/anaconda3/envs/boat_opencv_env/bin/python3
## !/home/boat-watcher/boatwatcher/boat_viewer/venv_boat_viewer/bin/python3
# This file is the entry point
import argparse
import sys
import camera
import utils.boat_viewer_utils as utils
import os

from datetime import datetime, timezone
import ephem
import time
# handles 

    # import necessary files and other modules
    # process arguments for program
    # call appropiate 


#### CONFIGURATIONS ####

# ## open images v7 full validation set of images
# DATASET_NAME = "open-images-v7"  #open_images_mini.yaml"
# DATASET_FRACTION = 1
# DATASET_SPLIT = "validation"
# DATASET_SPLIT_SIZE = 41620  # open-images-v7 val split 41620
# DATASET_PATH = f"./datasets/yolo/{DATASET_NAME}_{str(DATASET_FRACTION)}/images/{DATASET_SPLIT}/"
# DATASET_TRUTHS_PATH = f"./datasets/yolo/{DATASET_NAME}_{str(DATASET_FRACTION)}/labels/{DATASET_SPLIT}/"
# DATASET_BOAT_CLASS = 52

# coco 2017 full validation set of images
# DATASET_NAME = "coco-2017"  #open_images_mini.yaml"
# DATASET_FRACTION = 1
# DATASET_SPLIT = "validation"
# DATASET_SPLIT_SIZE = 5000 # coco val is 5000
# DATASET_PATH = f"./datasets/yolo/{DATASET_NAME}_{str(DATASET_FRACTION)}/images/{DATASET_SPLIT}/"
# DATASET_TRUTHS_PATH = f"./datasets/yolo/{DATASET_NAME}_{str(DATASET_FRACTION)}/labels/{DATASET_SPLIT}/"
# DATASET_BOAT_CLASS = 8 # 8 is boat


##### CONFIGURATION SELECTED ######
DATASET_NAME = "coco-2017"  #open_images_mini.yaml"
DATASET_FRACTION = 1
DATASET_SPLIT = "validation"
DATASET_SPLIT_SIZE = 5000 # coco val is 5000
DATASET_PATH = f"./datasets/yolo/{DATASET_NAME}_{str(DATASET_FRACTION)}/images/{DATASET_SPLIT}/"
DATASET_TRUTHS_PATH = f"./datasets/yolo/{DATASET_NAME}_{str(DATASET_FRACTION)}/labels/{DATASET_SPLIT}/"
DATASET_BOAT_CLASS = 8 # 8 is boat



MAX_IMAGES = -1   # A value of -1 corresponds to full dataset
if MAX_IMAGES == -1:
    if os.path.isdir(DATASET_PATH):
        MAX_IMAGES = len(os.listdir(DATASET_PATH))
    else:
        print("Warning: Dataset Not Created, setting default MAX IMAGES TO 100")
        MAX_IMAGES = 100

MODEL_NAME = "yolov5xu.pt"

CAPTURE_DATASET_TIME = 180  # minutes
CAPTURE_INTERVAL= 8 # seconds

CAPTURE_BOAT_TIME = 30/60 #minutes
CAPTURE_BOAT_INTERVAL= 10 # seconds


def main(args):
    # define main function
    #   RULE: main function must have only:
    # - argument parsing
    # -  high level lines of code

    # ARG IDEA LIST
    # - debug mode
    # - 
    # if args.one_image: 
        # one_image_routine(args)

    if args.one_image:
        print(f"PRE CAPTURE TIME:{datetime.today().strftime('%Y-%m-%d %H:%M:%S')}")
        camera.get_image(image_size="FULL")
        print(f"POST CAPTURE TIME:{datetime.today().strftime('%Y-%m-%d %H:%M:%S')}")

    elif args.capture_images:
        capture_images()

    elif args.boat_detector:
        while(1):
            if is_daylight():
                detect_boats(args.upload_images)
            else:
                time.sleep(30)
    # camera.get_image_all_apis()
    # camera.get_image_all_devices()

    elif args.get_dataset:
        utils.get_dataset(DATASET_NAME,DATASET_FRACTION,DATASET_SPLIT,DATASET_SPLIT_SIZE)

    elif args.model_testing:
        if args.multi_models:
            multi_model_testing()
        else:
            model_testing_routine(args.save_report)

    elif args.compress_dataset:
        camera.process_images_routine("./datasets/freeland_180_min_2025_04_12__17_06","datasets/freeland_180_min_2025_04_12__17_06_compressed")


    else:
        print("Error, nothing to do")

    print("DONE")


def detect_boats(upload_to_cloud):
    # pass
    # TODO: this will be a daemon that runs on pi and does it ALL
    # ---- take pictures, detect boats, and upload to AWS ----
    camera.get_image(image_size="MEDIUM",temp_image=True)
    boat_detected = utils.check_for_boat(MODEL_NAME, "temp_image.jpg",DATASET_BOAT_CLASS)
    if boat_detected:
        print("DETECTED BOAT!!")
        camera.get_many_images(CAPTURE_BOAT_TIME,f"./saved_boats/freeland_{datetime.today().strftime('%Y_%m_%d')}/",CAPTURE_BOAT_INTERVAL,upload_to_cloud)

def multi_model_testing():
    models = [ 	
    "yolov3-tinyu",
    "yolov3-sppu",
    "yolov3u",
    "yolov5nu",
    "yolov5su",
    "yolov5mu",
    "yolov5lu",
    "yolov5xu",
    "yolov5n6u",
    "yolov5s6u",
    "yolov5m6u",
    "yolov5l6u",
    "yolov5x6u",
    "yolov8n",
    "yolov8s",
    "yolov8m",
    "yolov8l",
    "yolov8x",
              ]
    models = [
    "yolov3u",
    "yolov8n",
    "yolov8x",

    ]
    datasets = [
        {"name":"coco-2017","fraction":.001,"split":"validation","split_size":5000,"boat_class":8 },
    ]
    # HEADER OUTPUT
    report_file = open("multi_model_test_report.txt", 'a')
    report_file.write("model_name,timestamp,dataset_name,dataset_split,dataset_fraction,num_images,boat_class,TP,FP,TN,FN,per_image_time\n")
    for dataset in datasets:
        dataset_path = f'./datasets/yolo/{dataset["name"]}_{str(dataset["fraction"])}/images/{dataset["split"]}/'
        max_images = int(dataset["split_size"]*dataset["fraction"])
        if not os.path.isdir(dataset_path):
            # acquire dataset
            utils.get_dataset(dataset["name"],dataset["fraction"],dataset["split"],dataset['split_size'])
            if not os.path.isdir(dataset_path):
                print("ERROR Getting Dataset")
                return

        for model in models:
            dataset_truth_path = f'./datasets/yolo/{dataset["name"]}_{str(dataset["fraction"])}/labels/{dataset["split"]}/'
            predictions,average_time = utils.get_predictions(model,dataset_path,max_images,dataset["boat_class"])
            truths  = utils.get_truths(dataset_truth_path,max_images)
            report = utils.compare_and_report(truths,predictions,dataset["boat_class"],max_images,brief=True)
            
            
            report_file.write(
                f"{model},"+\
                f"{datetime.today().strftime('%Y-%m-%d %H:%M:%S')},"+\
                f"{dataset['name']},"+\
                f"{dataset['split']},"+\
                f"{dataset['fraction']},"+\
                f"{max_images},"+\
                f"{dataset['boat_class']},"+\
                f"{report["true_positives"]},"+\
                f"{report["false_positives"]},"+\
                f"{report["true_negatives"]},"+\
                f"{report["false_negatives"]},"+\
                f"{average_time}\n")



            # report_file.write("#### MODEL REPORT ####\n")
            # report_file.write(f"DATE:{datetime.today().strftime('%Y-%m-%d %H:%M:%S')}\n")
            # report_file.write(f"MODEL_NAME:{model}\n")
            # report_file.write(f"DATASET_PATH:{dataset_path}\n")
            # report_file.write(f"DATASET_TRUTHS_PATH:{dataset_truth_path}\n")
            # report_file.write(f"DATASET_NAME:{dataset['name']}\n")
            # report_file.write(f"MAX_IMAGES:{max_images}\n")
            # report_file.write(f"PER_IMG_TIME:{average_time}\n")
            # for key, value in report.items():
            #     report_file.write(f"{key}:{value}\n")
            # report_file.write("#### END MODEL REPORT ####\n")
        


def model_testing_routine(save_report):

    predictions,average_time = utils.get_predictions(MODEL_NAME,DATASET_PATH,MAX_IMAGES)
    truths  = utils.get_truths(DATASET_TRUTHS_PATH,MAX_IMAGES)
    
    report = utils.compare_and_report(truths,predictions,DATASET_BOAT_CLASS,MAX_IMAGES)

    print(report)

    if save_report:
        report_file = open("model_test_report.txt", 'a')
        report_file.write("#### MODEL REPORT ####\n")
        report_file.write(f"DATE:{datetime.today().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report_file.write(f"MODEL_NAME:{MODEL_NAME}\n")
        report_file.write(f"DATASET_PATH:{DATASET_PATH}\n")
        report_file.write(f"DATASET_TRUTHS_PATH:{DATASET_TRUTHS_PATH}\n")
        report_file.write(f"DATASET_NAME:{DATASET_NAME}\n")
        report_file.write(f"MAX_IMAGES:{MAX_IMAGES}\n")
        for key, value in report.items():
            report_file.write(f"{key}:{value}\n")
        report_file.write("#### END MODEL REPORT ####\n")

 
def capture_images():
    pass ## TODO: Put the correct image here
    camera.get_many_images(CAPTURE_DATASET_TIME,f"./datasets/freeland_{CAPTURE_DATASET_TIME}_min_{datetime.today().strftime('%Y_%m_%d__%H_%M')}/",CAPTURE_INTERVAL)


def is_daylight():
    FREELAND_LAT = '47.92'
    FREELAND_LON = '-122.585'


    # Set observer location (Freeland, WA)
    observer = ephem.Observer()
    observer.lat = FREELAND_LAT
    observer.lon = FREELAND_LON
    observer.date = datetime.now(timezone.utc)  # current UTC time

    sun = ephem.Sun(observer)
    sun_altitude = sun.alt  # Altitude of the sun in radians

    return sun_altitude > 0 


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Python script boilerplate.")

    group = parser.add_mutually_exclusive_group(required=True)
    
    # PRIMARY ROUTINES
    group.add_argument("-o", "--one_image", help="Capture One Image", action='store_true')
    group.add_argument("-i", "--capture_images", help="Capture a bunch of images", action='store_true')
    group.add_argument("-m", "--model_testing", help="Measure Models on Datasets", action='store_true')
    group.add_argument("-b", "--boat_detector", help="Run whole boat detector system", action='store_true')
    group.add_argument("-d", "--get_dataset", help="Acquire the dataset", action='store_true')
    group.add_argument("-c", "--compress_dataset", help="Process Images to 640x640 for YOLO", action='store_true')
    
    # ADDITIONAL PARAMETERS / SETTINGS

    # parser.add_argument('--verbose', action='store_true', help='DEBUG: Enable verbose output')
    parser.add_argument('--save_report', action='store_true', help='add report to model_test_report.txt')
    parser.add_argument("-u",'--upload_images', action='store_true', help='upload boat images and delete if upload is successful')
    parser.add_argument('--multi_models', action='store_true', help='download, evaluate, and report multiple models')
    # parser.add_argument("-e",'--daytime_', action='store_true', help='run only when not in civil twilight')
    

    args = parser.parse_args()

    try:
        main(args)
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
        sys.exit(1)


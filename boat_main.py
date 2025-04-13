#!/opt/anaconda3/envs/boat_opencv_env/bin/python3
## !/home/boat-watcher/boatwatcher/boat_viewer/venv_boat_viewer/bin/python3
# This file is the entry point
import argparse
import sys
import camera
import utils.boat_viewer_utils as utils
import os
from datetime import datetime
# handles 

    # import necessary files and other modules
    # process arguments for program
    # call appropiate 

# DATASET_PATH = "/Users/samuel/git/boat_viewer/datasets/open-images-v7/images/train"
DATASET_PATH = "./datasets/open-images-v7/images/train"
DATASET_TRUTHS_PATH = "./datasets/open-images-v7/labels/train"
DATASET_YAML = "open_images_mini.yaml"
MAX_IMAGES = 100 #len(os.listdir(DATASET_PATH))
MODEL_NAME = "yolov8n-oiv7.pt"

CAPTURE_DATASET_TIME = 180  # minutes

CAPTURE_INTERVAL= 8 # seconds

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
        camera.get_image()
        print(f"POST CAPTURE TIME:{datetime.today().strftime('%Y-%m-%d %H:%M:%S')}")

    elif args.capture_images:
        capture_images()

    elif args.boat_detector:
        detect_boats()
    # camera.get_image_all_apis()
    # camera.get_image_all_devices()
    elif args.model_testing:
        model_testing_routine(args.save_report)

    else:
        print("Error, nothing to do")

    print("DONE")

def detect_boats():
    pass
    # TODO: this will be a daemon that runs on pi and does it ALL
    # ---- take pictures, detect boats, and upload to AWS ----
    

def model_testing_routine(save_report):

    predictions = utils.get_predictions(MODEL_NAME,DATASET_PATH,MAX_IMAGES)
    truths  = utils.get_truths(DATASET_TRUTHS_PATH,MAX_IMAGES)
    
    report = utils.compare_and_report(truths,predictions,52,MAX_IMAGES)

    print(report)

    if save_report:
        report_file = open("model_test_report.txt", 'a')
        report_file.write("#### MODEL REPORT ####\n")
        report_file.write(f"DATE:{datetime.today().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report_file.write(f"MODEL_NAME:{MODEL_NAME}\n")
        report_file.write(f"DATASET_PATH:{DATASET_PATH}\n")
        report_file.write(f"DATASET_TRUTHS_PATH:{DATASET_TRUTHS_PATH}\n")
        report_file.write(f"DATSET_YAML:{DATASET_YAML}\n")
        report_file.write(f"MAX_IMAGES:{MAX_IMAGES}\n")
        for key, value in report.items():
            report_file.write(f"{key}:{value}\n")
        report_file.write("#### END MODEL REPORT ####\n")


    

    
def capture_images():
    pass ## TODO: Put the correct image here
    camera.get_many_images(CAPTURE_DATASET_TIME,f"./datasets/freeland_{CAPTURE_DATASET_TIME}_min_{datetime.today().strftime('%Y_%m_%d__%H_%M')}/",CAPTURE_INTERVAL)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Python script boilerplate.")

    group = parser.add_mutually_exclusive_group(required=True)
    
    # PRIMARY ROUTINES
    group.add_argument("-o", "--one_image", help="Capture One Image", action='store_true')
    group.add_argument("-i", "--capture_images", help="Capture a bunch of images", action='store_true')
    group.add_argument("-m", "--model_testing", help="Measure Models on Datasets", action='store_true')
    group.add_argument("-b", "--boat_detector", help="Run whole boat detector system", action='store_true')
    
    # ADDITIONAL PARAMETERS / SETTINGS

    # parser.add_argument('--verbose', action='store_true', help='DEBUG: Enable verbose output')
    parser.add_argument('--save_report', action='store_true', help='add report to model_test_report.txt')
    

    args = parser.parse_args()

    try:
        main(args)
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
        sys.exit(1)

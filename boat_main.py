#!/opt/anaconda3/envs/boat_opencv_env/bin/python3
## !/home/boat-watcher/boatwatcher/boat_viewer/venv_boat_viewer/bin/python3
# This file is the entry point
import argparse
import sys
import camera
import utils.boat_viewer_utils as utils
# handles 

    # import necessary files and other modules
    # process arguments for program
    # call appropiate 

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

    # camera.get_image_all_apis()
    # camera.get_image_all_devices()
    model_name = "yolov8n-oiv7.pt"
    predictions = utils.get_predictions(model_name)

    truths  = utils.get_truths("open_images_mini.yaml")
    utils.compare_and_report(truths,predictions,52)


    
def one_image_routine(args):
    camera.get_image()
    # camera.gphoto_capture()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Python script boilerplate.")
    parser.add_argument("-n", "--name", type=str, help="Your name")
    parser.add_argument("-o", "--one_image", help="Capture One Image", action='store_true')
    args = parser.parse_args()

    try:
        main(args)
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
        sys.exit(1)

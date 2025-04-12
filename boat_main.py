#!/opt/anaconda3/envs/boat_opencv_env/bin/python3
## !/home/boat-watcher/boatwatcher/boat_viewer/venv_boat_viewer/bin/python3
# This file is the entry point
import argparse
import sys
import camera
import yolo_v8.yolov8n as yolov8n
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
    predictions = yolov8n.get_predictions(model_name)
    print(predictions)


    
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

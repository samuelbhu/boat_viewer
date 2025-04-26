# boat_viewer
## Program to capture images from a boat and upload them
---
Program run on the raspberry Pi
### Summary
This is the software for a boat photography project. The aim is to snap pictures of boats when they pass in front of a video camera. 
The software was built to run on the Raspberry Pi 5, but it has also been tested on MacOS and the machine learning components work on WSL.

### 
This is a Python

### Libraries Used
#### OpenCV 
Open CV is used to operate the camera and for any image transformations that may be desired.

#### FiftyOne
Fifty-One is used to acquire image datasets for model testing. It uses the FiftyOne Dataset Zoo to get the images and convert them to the YOLO dataset format. Custom testing functions tailored to this project needs are used to evaluate prediction quality.

#### Ultralytics
The Ultralytics library is used to provide the YOLO model for boat detection. It provides an easy-to-use interface to do many ML tasks for different YOLO models. It can directly aquire many of pretrained YOLO models. 

### Modes

#### Main Photography Daemon

##### Invoked with -b or --boat_detector

This is the primary photographing routine intended to run indefinitely. It saves and uploads pictures when boats come by. The daemon sleeps when the sun is down.
1. [Scanning] The system scans for a boat using the camera on the RPi, this is achieved by quickly capturing a lower resolution image and saving it to a reused temporary location. 
2. [Detecton] Each quick capture is sent for a single pass through a pre-trained YOLO ML model using Ultralytics. This is where the bulk of computing happens. Basic optimizations are made for the grouping of related images to help reduce duplicated captures.
3. [Photographing] If a boat is identified by YOLO a series of images are saved so that a few shots of a boat can be detected. 
4. [Loop] Once the photographing stage is complete it moves back to the scanning stage


#### Dataset Acquisition and Preparation
##### -d or --get_dataset

The dataset set in DATASET_NAME is acquired and converted to the YOLO format using FiftyOne with routines provided by Ultralytics.
##### -c or --compress_dataset
This uses OpenCV to modify a folder of images to be 640x640 to prepare them for use with YOLO. This routine can be modified in many ways to do other image processing. 

#### Model Testing
##### Invoked with -m or --model_testing

This uses pre defined values in boat_main.py to acquire a dataset and model and then report boat detection metrics. A multiple-model option is being developed to speed up model analysis. A dataset in the YOLO format is needed for this mode and can be acquired with the --get_dataset mode. 

##### Invoked with -o or --one_image
This is used to capture a single image at full camera resolution (8MP)

#### Imaging 
#####  -i or --capture_images
Used to create a real-world dataset. This will collect and save images from a camera for a set period of time and frequency and put them into a dated folder. Manual labeling will still be needed!
#####  -o or --one_image
This is used to capture a single image at full camera resolution (8MP)

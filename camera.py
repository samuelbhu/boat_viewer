import cv2
import os
import glob
import subprocess
import time
from datetime import datetime,timedelta
import utils.boat_viewer_utils as utils

WARMUP_FRAMES=3

def get_image(cam=None,folder=".",image_size="FULL",temp_image=False):

    if not cam:
        cam_port=1
        cam = cv2.VideoCapture(cam_port,cv2.CAP_ANY)
        cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

    if not cam.isOpened():
        print(f"Error: Cannot open camera at index {cam_port}")
        return None

    if(image_size=="SMALL"):
        # save small image
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, 800)  
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 600) 
        cam.set(cv2.CAP_PROP_BRIGHTNESS,35)
    elif(image_size=="MEDIUM"): # 
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1600)  
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1200) 
        cam.set(cv2.CAP_PROP_BRIGHTNESS,55)

    elif(image_size=="FULL"):
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, 3264)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 2448)

        # cam.set(cv2.CAP_PROP_BRIGHTNESS,10)
    
    # OPTIONAL CAMERA SETTINGS
    # cam.set(cv2.CAP_PROP_BRIGHTNESS, 10.0)
    # cam.set(cv2.CAP_PROP_CONTRAST, 15.0)
    # cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3.0)


    for _ in range(WARMUP_FRAMES):
        cam.read()
        time.sleep(0.1)

    result, image = cam.read() 
    if temp_image:
        filename = "temp_image"
    
    else:
        filename = f"image_{datetime.today().strftime('%Y-%m-%d_%H:%M:%S')}"

    if result:
        print(f"writing to folder:{folder}{filename}.jpg")
        cv2.imwrite(f"{folder}/{filename}.jpg", image)  # Save the captured image
    else:
        print("Error: Failed to capture image.")
    return filename


def get_many_images(camera_obj, runtime_mins,folder,interval_secs,upload):
    # runtime_mins:  how many minutes to run image capture 
    # capture_rate_secs:  how many seconds per capture
    print(f"folder{folder}")
    os.makedirs(os.path.dirname(folder), exist_ok=True)

    duration = timedelta(minutes=runtime_mins)
    start_time = datetime.now()
    end_time = start_time + duration    
    
    while datetime.now() < end_time:
        capture_start = datetime.now()
        filename = get_image(
            cam=camera_obj, 
            folder=folder,
            image_size="MEDIUM"
        
        )
        if upload:
            if utils.upload_image(f"{folder}{filename}.jpg"):
                utils.delete_image(f"{folder}{filename}.jpg")
            else:
                print(f"Did not successfully upload{filename}")

        capture_end = datetime.now()
        # Your image capture or routine goes here
        print("Captured image at", capture_end)
        capture_duration = (capture_end - capture_start).total_seconds()
        # Wait for 7.65 seconds (or your calculated interval)
        time.sleep(max(0,interval_secs-capture_duration))


def get_image_all_apis():
    api_list = [
    ("CAP_ANY",cv2.CAP_ANY),
    ("CAP_VFW",cv2.CAP_VFW),
    ("CAP_V4L",cv2.CAP_V4L),
    ("CAP_V4L2",cv2.CAP_V4L2),
    ("CAP_FIREWIRE",cv2.CAP_FIREWIRE),
    ("CAP_FIREWARE",cv2.CAP_FIREWARE),
    ("CAP_IEEE1394",cv2.CAP_IEEE1394),
    ("CAP_DC1394",cv2.CAP_DC1394),
    ("CAP_CMU1394",cv2.CAP_CMU1394),
    ("CAP_QT",cv2.CAP_QT),
    ("CAP_UNICAP",cv2.CAP_UNICAP),
    ("CAP_DSHOW",cv2.CAP_DSHOW),
    ("CAP_PVAPI",cv2.CAP_PVAPI),
    ("CAP_OPENNI",cv2.CAP_OPENNI),
    ("CAP_OPENNI_ASUS",cv2.CAP_OPENNI_ASUS),
    ("CAP_ANDROID",cv2.CAP_ANDROID),
    ("CAP_XIAPI",cv2.CAP_XIAPI),
    ("CAP_AVFOUNDATION",cv2.CAP_AVFOUNDATION),
    ("CAP_GIGANETIX",cv2.CAP_GIGANETIX),
    ("CAP_MSMF",cv2.CAP_MSMF),
    ("CAP_WINRT",cv2.CAP_WINRT),
    ("CAP_INTELPERC",cv2.CAP_INTELPERC),
    ("CAP_OPENNI2",cv2.CAP_OPENNI2),
    ("CAP_OPENNI2_ASUS",cv2.CAP_OPENNI2_ASUS),
    ("CAP_GPHOTO2",cv2.CAP_GPHOTO2),
    ("CAP_GSTREAMER",cv2.CAP_GSTREAMER),
    ("CAP_FFMPEG",cv2.CAP_FFMPEG),
    ("CAP_IMAGES",cv2.CAP_IMAGES),
    ("CAP_ARAVIS",cv2.CAP_ARAVIS),
    ("CAP_OPENCV_MJPEG",cv2.CAP_OPENCV_MJPEG),
    ("CAP_INTEL_MFX",cv2.CAP_INTEL_MFX),
    ("CAP_XINE",cv2.CAP_XINE),
    ]
    for api in api_list:
        cam_port=0
        cam = cv2.VideoCapture(cam_port,api[1])
        print("Api%s"%(api[0]))
        max_width, max_height = get_max_resolution(cam)
        print("maxwidth:%d, height:%d"%(max_width,max_height))
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, 3264)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 2448)

        # cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)  # Set width
        # cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)  # Set height
        
        result, image = cam.read() 



        if result:
            cv2.imwrite("captured_image_%s.jpg"%(api[0]), image)  # Save the captured image
        else:
            print("Error: Failed to capture image.%s"%(api[0]))




def get_max_resolution(cap):
    """Gets the maximum resolution supported by the device."""
    max_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    max_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    return max_width, max_height


def get_image_all_devices():
    devices = list_video_devices()
    if not devices:
        print("No video devices found.")
    else:
        for device in devices:
            capture_image_from_device(device)    

def list_video_devices():
    """Lists available video devices on Linux."""
    return glob.glob('/dev/video*')

def gphoto_capture():
    cameras = list_gphoto2_devices()
    if not cameras:
        print("No cameras found.")
    else:
        for camera in cameras:
            capture_image_from_camera(camera)


def list_gphoto2_devices():
    """Lists available cameras using gphoto2."""
    try:
        result = subprocess.run(["gphoto2", "--auto-detect"], capture_output=True, text=True)
        lines = result.stdout.split("\n")[2:]  # Skip header lines
        devices = [line.split("\t")[-1] for line in lines if line.strip()]
        return devices
    except FileNotFoundError:
        print("gphoto2 not found. Please install it using: sudo apt install gphoto2")
        return []

def capture_image_from_camera(camera_name):
    """Captures an image from the specified camera using gphoto2."""
    filename = f"image_device_{camera_name.replace(' ', '_')}.jpg"
    try:
        subprocess.run(["gphoto2", "--capture-image-and-download", "--filename", filename], check=True)
        print(f"Saved image: {filename}")
    except subprocess.CalledProcessError:
        print(f"Failed to capture image from {camera_name}")


def capture_image_from_device(device_path):
    """Captures an image from the specified video device."""
    index = int(device_path.replace('/dev/video', ''))  # Extract index
    cap = cv2.VideoCapture(index)
    
    if not cap.isOpened():
        print(f"Could not open {device_path}")
        return
    
    ret, frame = cap.read()
    cap.release()
    
    if ret:
        filename = f"image_device_{os.path.basename(device_path)}.jpg"
        cv2.imwrite(filename, frame)
        print(f"Saved image: {filename}")
    else:
        print(f"Failed to capture image from {device_path}")

def process_images_routine(input_folder,output_folder):
    # this is going to do some processing of taken images
    # import cv2
    # import os

    # input_folder = "path_to_your_images"
    # output_folder = "path_to_compressed_images"

    crop_factor = 0.1

    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.endswith((".jpg", ".jpeg", ".png")):
            img_path = os.path.join(input_folder, filename)
            img = cv2.imread(img_path)

            # RESIZE TO SQUARE
            # Get dimensions and determine the square crop
            height, width = img.shape[:2]
            min_dim = min(height, width)
            start_x = (width - min_dim) // 2
            start_y = (height - min_dim) // 2
            square_cropped_img = img[start_y:start_y + min_dim, start_x:start_x + min_dim]
            
            # CROP BY A FACTOR
            height, width = square_cropped_img.shape[:2]
            crop_x = int(width * crop_factor)
            crop_y = int(height * crop_factor)
            # Crop the image (remove crop_factor portions from all sides)
            cropped_img = img[crop_y:height - crop_y, crop_x:width - crop_x]
            
            # Resize to YOLO-compatible dimensions after cropping
            resized_img = cv2.resize(cropped_img, (640, 640))            

            # resized_img = cv2.resize(square_cropped_img, (640, 640))  # Resize to YOLO dimensions


            compressed_img_path = os.path.join(output_folder, filename)
            cv2.imwrite(compressed_img_path, resized_img, [cv2.IMWRITE_JPEG_QUALITY, 100])  # Compress and save
        # input("one_done")


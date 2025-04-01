import cv2
import os
import glob
import subprocess

def get_image():
    cam_port=1
    small_img = True
    # cam = cv2.VideoCapture(cam_port,cv2.CAP_V4L2)
    cam = cv2.VideoCapture(cam_port,cv2.CAP_ANY)
    
    max_width, max_height = get_max_resolution(cam)
    print("maxwidth:%d, height:%d"%(max_width,max_height))
    if(small_img):
        # save roughly a quarter size of image
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, 800)  # Set width
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)  # Set height
        # cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3.0)
        cam.set(cv2.CAP_PROP_BRIGHTNESS,30)

    else:
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, 3264)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 2448)
        # cam.set(cv2.CAP_PROP_BRIGHTNESS, 1.0)
        # cam.set(cv2.CAP_PROP_CONTRAST, 1.0)

    set_test = True
    if set_test:
        set_item = (cv2.CAP_PROP_FOURCC, 2)

        # cam.set(set_item[0],set_item[1])
        print(cam.get(set_item[0]))


    

    result, image = cam.read() 
    result, image = cam.read() 
    result, image = cam.read() 
    result, image = cam.read() 
    result, image = cam.read() 
    result, image = cam.read() 
    result, image = cam.read() 
    result, image = cam.read() 



    if result:
        cv2.imwrite("single_captured_image.jpg", image)  # Save the captured image
    else:
        print("Error: Failed to capture image.")

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
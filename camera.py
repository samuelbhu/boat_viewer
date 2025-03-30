import cv2
import os
import glob
import subprocess
def get_image():
    cam_port=0
    cam = cv2.VideoCapture(cam_port,cv2.CAP_V4L2)
    
    max_width, max_height = get_max_resolution(cam)
    print("maxwidth:%d, height:%d"%(max_width,max_height))
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 20)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 20)

    # cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)  # Set width
    # cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)  # Set height
    
    result, image = cam.read() 



    if result:
        cv2.imwrite("captured_image.jpg", image)  # Save the captured image
    else:
        print("Error: Failed to capture image.")


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
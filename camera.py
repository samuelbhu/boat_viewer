import cv2

def get_image():
    cam_port=0
    cam = cv2.VideoCapture(cam_port)

    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)  # Set width
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)  # Set height
    
    result, image = cam.read() 



    if result:
        cv2.imwrite("captured_image.jpg", image)  # Save the captured image
    else:
        print("Error: Failed to capture image.")
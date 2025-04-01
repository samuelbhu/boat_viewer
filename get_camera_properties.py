import cv2

def get_camera_properties(camera_index=0):
    cam = cv2.VideoCapture(camera_index)
    
    if not cam.isOpened():
        print("Error: Could not open camera.")
        return {}
    properties = {
        "POS_MSEC": 0,
        "POS_FRAMES": 1,
        "POS_AVI_RATIO": 2,
        "FRAME_WIDTH": 3,
        "FRAME_HEIGHT": 4,
        "FPS": 5,
        "FOURCC": 6,
        "FRAME_COUNT": 7,
        "FORMAT": 8,
        "MODE": 9,
        "BRIGHTNESS": 10,
        "CONTRAST": 11,
        "SATURATION": 12,
        "HUE": 13,
        "GAIN": 14,
        "EXPOSURE": 15,
        "CONVERT_RGB": 16,
        "WHITE_BALANCE_BLUE_U": 17,
        "RECTIFICATION": 18,
        "MONOCHROME": 19,
        "SHARPNESS": 20,
        "AUTO_EXPOSURE": 21,
        "GAMMA": 22,
        "TEMPERATURE": 23,
        "TRIGGER": 24,
        "TRIGGER_DELAY": 25,
        "WHITE_BALANCE_RED_V": 26,
        "ZOOM": 27,
        "FOCUS": 28,
        "GUID": 29,
        "ISO_SPEED": 30,
        "BACKLIGHT": 32,
        "PAN": 33,
        "TILT": 34,
        "ROLL": 35,
        "IRIS": 36,
        "SETTINGS": 37,
        "BUFFERSIZE": 38,
        "AUTOFOCUS": 39,
        "SAR_NUM": 40,
        "SAR_DEN": 41,
        "BACKEND": 42,
        "CHANNEL": 43,
        "AUTO_WB": 44,
        "WB_TEMPERATURE": 45,
        "CODEC_PIXEL_FORMAT": 46,
        "BITRATE": 47,
        "ORIENTATION_META": 48,
        "ORIENTATION_AUTO": 49,
        "OPEN_TIMEOUT_MSEC": 53,
        "READ_TIMEOUT_MSEC": 54
    }
    
    # Query the properties
    camera_properties = {prop: cam.get(value) for prop, value in properties.items()}
    
    cam.release()
    return camera_properties

if __name__ == "__main__":
    props = get_camera_properties()
    for key, value in props.items():
        print(f"{key}: {value}")

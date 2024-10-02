import cv2
import numpy as np
import time
import datetime
import platform_decider

def capture_multiple_screenshots(os_id, num_screenshots=60, interval=1):
    total_brightness = 0
    valid_captures = 0
    # CAP_DSHOW is a windows-thing
    video_flag = cv2.CAP_DSHOW
    if "linux" in os_id:
        video_flag = cv2.CAP_V4L2

    cam = cv2.VideoCapture(0, video_flag)

    if not cam.isOpened():
        log("Camera is not accessible. It may be in use by another application.")
        return 0

    for _ in range(num_screenshots):
        ret, frame = cam.read()
        if not ret:
            #print("Failed to capture image from webcam")
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        avg_brightness = np.mean(gray)

        if avg_brightness == 0:
            #print("Captured image is completely black. Skipping this capture.")
            continue

        total_brightness += avg_brightness
        valid_captures += 1

        time.sleep(interval)

    cam.release()

    if valid_captures == 0:
        print("No valid captures were made.")
        return 0

    average_brightness = total_brightness / valid_captures
    log(f"Average brightness from {valid_captures} captures: {average_brightness}")

    return average_brightness

def detect_brightness_and_switch_theme(os_id):
    avg_brightness = capture_multiple_screenshots(os_id)

    if avg_brightness == 0:
        print("Failed to calculate average brightness. Maybe the camera is used by another application.")
        return

    brightness_threshold = get_time_based_threshold()
    current_theme = platform_decider.get_theme(os_id)
    new_theme = ""
    if avg_brightness < brightness_threshold:
        log(f"Switching to Dark Mode.")
        new_theme = "dark"
    else:

        log(f"Switching to Light Mode.")
        new_theme = "light"

    if new_theme != current_theme:
        platform_decider.set_theme(os_id, new_theme)

def get_time_based_threshold():
    current_hour = datetime.datetime.now().hour

    if 6 <= current_hour < 12:  # Morning (6 AM to 12 PM)
        return 90
    elif 12 <= current_hour < 18:  # Afternoon (12 PM to 6 PM)
        return 85
    elif 18 <= current_hour < 21:  # Evening (6 PM to 9 PM)
        return 90
    else:  # Night (9 PM to 6 AM)
        return 105

def log(message):
    print(f"[{datetime.datetime.now()}] {message}")

if __name__ == "__main__":
    os_id = platform_decider.get_os_id()
    log(f"Found {os_id} Environment")
    detect_brightness_and_switch_theme(os_id)

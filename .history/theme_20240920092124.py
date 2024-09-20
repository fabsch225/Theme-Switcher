import cv2
import numpy as np
import subprocess

def detect_brightness_and_switch_theme():
    # Capture image from webcam
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    cam.release()

    if not ret:
        print("Failed to capture image from webcam.")
        return

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Calculate the average brightness
    avg_brightness = np.mean(gray)

    # Define a threshold for brightness (this will depend on your room conditions)
    brightness_threshold = 100

    # Check the brightness and switch theme accordingly
    if avg_brightness < brightness_threshold:
        # Run the PowerShell script to switch to dark mode
        subprocess.run(["powershell", "-Command", "Set-ItemProperty -Path HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize -Name AppsUseLightTheme -Value 0"])
        print(f"Switched to Dark Mode. Avg Brightness: {avg_brightness}")
    else:
        # Run the PowerShell script to switch to light mode
        subprocess.run(["powershell", "-Command", "Set-ItemProperty -Path HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize -Name AppsUseLightTheme -Value 1"])
        print(f"Switched to Light Mode. Avg Brightness: {avg_brightness}")

if __name__ == "__main__":
    detect_brightness_and_switch_theme()

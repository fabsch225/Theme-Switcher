import cv2
import numpy as np
import subprocess

# Capture image from webcam
cam = cv2.VideoCapture(0)
ret, frame = cam.read()
cam.release()

# Convert to grayscale
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Calculate the average brightness
avg_brightness = np.mean(gray)

# Define a threshold for brightness (this will depend on your lighting conditions)
brightness_threshold = 100

if avg_brightness < brightness_threshold:
    # Run the PowerShell script to switch to dark mode
    subprocess.run(["powershell", "-Command", "Set-ItemProperty -Path HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize -Name AppsUseLightTheme -Value 0"])
else:
    # Run the PowerShell script to switch to light mode
    subprocess.run(["powershell", "-Command", "Set-ItemProperty -Path HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize -Name AppsUseLightTheme -Value 1"])

import cv2
import numpy as np
import subprocess

cam = cv2.VideoCapture(0)
ret, frame = cam.read()
cam.release()

gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

avg_brightness = np.mean(gray)

brightness_threshold = 100

if avg_brightness < brightness_threshold:  
    subprocess.run(["powershell", "-Command", "Set-ItemProperty -Path HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize -Name AppsUseLightTheme -Value 0"])
else:
    subprocess.run(["powershell", "-Command", "Set-ItemProperty -Path HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize -Name AppsUseLightTheme -Value 1"])

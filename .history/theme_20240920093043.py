import cv2
import numpy as np
import subprocess

def restart_explorer():
    # Kill and restart explorer.exe to apply the theme change
    subprocess.run(["powershell", "-Command", "Stop-Process -Name explorer -Force"])
    time.sleep(1)  # Give it a second to fully stop
    subprocess.run(["powershell", "-Command", "Start-Process explorer"])


def detect_brightness_and_switch_theme():
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    cam.release()

    if not ret:
        print("Failed to capture image from webcam.")
        return

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

   avg_brightness = np.mean(gray)

    brightness_threshold = 100

    if avg_brightness < brightness_threshold:
        subprocess.run(["powershell", "-Command", "Set-ItemProperty -Path HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize -Name AppsUseLightTheme -Value 0"])
        print(f"Switched to Dark Mode. Avg Brightness: {avg_brightness}")
    else:
        subprocess.run(["powershell", "-Command", "Set-ItemProperty -Path HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize -Name AppsUseLightTheme -Value 1"])
        print(f"Switched to Light Mode. Avg Brightness: {avg_brightness}")

if __name__ == "__main__":
    detect_brightness_and_switch_theme()

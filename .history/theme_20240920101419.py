import cv2
import numpy as np
import subprocess

def broadcast_theme_change():
    HWND_BROADCAST = 0xFFFF
    WM_SETTINGCHANGE = 0x001A
    WM_THEMECHANGED = 0x031A  
    WM_STYLECHANGED = 0x007D
    WM_NCPAINT = 0x0085
    WM_PAINT = 0x000F

    ctypes.windll.user32.SendMessageTimeoutW(HWND_BROADCAST, WM_SETTINGCHANGE, 0, 'ImmersiveColorSet', 0, 5000, None)
    ctypes.windll.user32.SendMessageTimeoutW(HWND_BROADCAST, WM_THEMECHANGED, 0, 0, 0, 5000, None)
    ctypes.windll.user32.SendMessageTimeoutW(HWND_BROADCAST, WM_STYLECHANGED, 0, 0, 0, 5000, None)
    #ctypes.windll.user32.SendMessageTimeoutW(HWND_BROADCAST, WM_NCPAINT, 0, 0, 0, 5000, None)
    #ctypes.windll.user32.SendMessageTimeoutW(HWND_BROADCAST, WM_PAINT, 0, 0, 0, 5000, None)


def restart_explorer():
    subprocess.run(["powershell", "-Command", "Stop-Process -Name explorer"])

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

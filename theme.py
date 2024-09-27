import cv2
import ctypes
import numpy as np
import time
import datetime
import winreg
import subprocess
import threading

def broadcast_theme_change():
    HWND_BROADCAST = 0xFFFF
    WM_SETTINGCHANGE = 0x001A
    WM_THEMECHANGED = 0x031A  
    WM_STYLECHANGED = 0x007D
    WM_NCPAINT = 0x0085
    WM_PAINT = 0x000F

    ctypes.windll.user32.SendMessageTimeoutW(HWND_BROADCAST, WM_SETTINGCHANGE, 0, 'ImmersiveColorSet', 0, 5000, None)
    #ctypes.windll.user32.SendMessageTimeoutW(HWND_BROADCAST, WM_THEMECHANGED, 0, 0, 0, 5000, None)
    #ctypes.windll.user32.SendMessageTimeoutW(HWND_BROADCAST, WM_STYLECHANGED, 0, 0, 0, 5000, None)
    #ctypes.windll.user32.SendMessageTimeoutW(HWND_BROADCAST, WM_NCPAINT, 0, 0, 0, 5000, None)
    #ctypes.windll.user32.SendMessageTimeoutW(HWND_BROADCAST, WM_PAINT, 0, 0, 0, 5000, None)

def restart_explorer():
    subprocess.run(["powershell", "-Command", "Stop-Process -Name explorer"])

def get_current_theme():
    try:
        # Open the registry key for theme settings
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize") as key:
            apps_use_light_theme = winreg.QueryValueEx(key, "AppsUseLightTheme")[0]
            system_uses_light_theme = winreg.QueryValueEx(key, "SystemUsesLightTheme")[0]
            
            # Determine the current theme
            if apps_use_light_theme == 1 and system_uses_light_theme == 1:
                return "light"
            elif apps_use_light_theme == 0 and system_uses_light_theme == 0:
                return "dark"
            else:
                return "unknown"
    except Exception as e:
        log(f"Error accessing the registry: {e}")
        return "unknown"

def capture_multiple_screenshots(num_screenshots=120, interval=1):
    """Capture multiple screenshots and calculate average brightness."""
    total_brightness = 0
    valid_captures = 0

    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cam.isOpened():
        log("Camera is not accessible. It may be in use by another application.")
        return

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

        time.sleep(interval)  # Wait for the specified interval

    cam.release()

    if valid_captures == 0:
        print("No valid captures were made.")
        return 0

    average_brightness = total_brightness / valid_captures
    log(f"Average brightness from {valid_captures} captures: {average_brightness}")

    return average_brightness

def detect_brightness_and_switch_theme():
    avg_brightness = capture_multiple_screenshots()

    if avg_brightness == 0:
        log("Failed to calculate average brightness. Maybe the camera is used by another application.")
        return

    brightness_threshold = 85
    current_theme = get_current_theme()
    new_theme = ""

    if avg_brightness < brightness_threshold:
        subprocess.run([
            "powershell", "-Command",
            "Set-ItemProperty -Path HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize -Name AppsUseLightTheme -Value 0;"
            "Set-ItemProperty -Path HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize -Name SystemUsesLightTheme -Value 0"
        ])
        log(f"Switched to Dark Mode.")
        new_theme = "dark"
    else:
        subprocess.run([
            "powershell", "-Command",
            "Set-ItemProperty -Path HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize -Name AppsUseLightTheme -Value 1;"
            "Set-ItemProperty -Path HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize -Name SystemUsesLightTheme -Value 1"
        ])
        log(f"Switched to Light Mode.")
        new_theme = "light"

    if (new_theme != current_theme):
        thread = threading.Thread(target=broadcast_theme_change)
        thread.start()
        restart_explorer()

def log(message):
    print(f"[{datetime.datetime.now()}] {message}")

if __name__ == "__main__":
    detect_brightness_and_switch_theme()

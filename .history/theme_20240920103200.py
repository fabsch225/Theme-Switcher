import cv2
import ctypes
import numpy as np
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
    ctypes.windll.user32.SendMessageTimeoutW(HWND_BROADCAST, WM_THEMECHANGED, 0, 0, 0, 5000, None)
    ctypes.windll.user32.SendMessageTimeoutW(HWND_BROADCAST, WM_STYLECHANGED, 0, 0, 0, 5000, None)
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
        print(f"Error accessing the registry: {e}")
        return "unknown"

def detect_brightness_and_switch_theme():
    global theme
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    ret, frame = cam.read()
    cam.release()

    if not ret:
        print("Failed to capture image from webcam.")
        return

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    avg_brightness = np.mean(gray)
    brightness_threshold = 100
    new_theme = theme

    if avg_brightness < brightness_threshold:
        subprocess.run([
            "powershell", "-Command",
            "Set-ItemProperty -Path HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize -Name AppsUseLightTheme -Value 0;"
            "Set-ItemProperty -Path HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize -Name SystemUsesLightTheme -Value 0"
        ])
        print(f"Switched to Dark Mode. Avg Brightness: {avg_brightness}")
        new_theme = "dark"
    else:
        subprocess.run([
            "powershell", "-Command",
            "Set-ItemProperty -Path HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize -Name AppsUseLightTheme -Value 1;"
            "Set-ItemProperty -Path HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize -Name SystemUsesLightTheme -Value 1"
        ])
        print(f"Switched to Light Mode. Avg Brightness: {avg_brightness}")
        new_theme = "light"

    if (new_theme != theme):
        theme = new_theme
        thread = threading.Thread(target=broadcast_theme_change)
        thread.start()
        restart_explorer()


if __name__ == "__main__":
    detect_brightness_and_switch_theme()

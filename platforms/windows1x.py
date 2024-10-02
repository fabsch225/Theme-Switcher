import winreg
import ctypes
import subprocess
from main import log
import threading

def change_mode(mode):
    if mode == "dark":
        subprocess.run([
            "powershell", "-Command",
            "Set-ItemProperty -Path HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize -Name AppsUseLightTheme -Value 0;"
            "Set-ItemProperty -Path HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize -Name SystemUsesLightTheme -Value 0"
        ])
    elif mode == "light":
        subprocess.run([
            "powershell", "-Command",
            "Set-ItemProperty -Path HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize -Name AppsUseLightTheme -Value 1;"
            "Set-ItemProperty -Path HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize -Name SystemUsesLightTheme -Value 1"
        ])

    thread = threading.Thread(target=broadcast_theme_change)
    thread.start()
    restart_explorer()

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
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize") as key:
            apps_use_light_theme = winreg.QueryValueEx(key, "AppsUseLightTheme")[0]
            system_uses_light_theme = winreg.QueryValueEx(key, "SystemUsesLightTheme")[0]

            if apps_use_light_theme == 1 and system_uses_light_theme == 1:
                return "light"
            elif apps_use_light_theme == 0 and system_uses_light_theme == 0:
                return "dark"
            else:
                return "unknown"
    except Exception as e:
        log(f"Error accessing the registry: {e}")
        return "unknown"
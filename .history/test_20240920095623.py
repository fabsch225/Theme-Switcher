import ctypes
import subprocess
import time

# Constants for broadcasting WM_THEMECHANGED
HWND_BROADCAST = 0xFFFF
WM_THEMECHANGED = 0x031A  # Message constant for WM_THEMECHANGED

# Function to broadcast WM_THEMECHANGED message to all windows
def broadcast_theme_change():
    ctypes.windll.user32.SendMessageTimeoutW(HWND_BROADCAST, WM_THEMECHANGED, 0, 0, 0, 5000, None)

def switch_theme(dark_mode=True):
    # Switch between dark and light mode in the registry
    if dark_mode:
        subprocess.run([
            "powershell", "-Command",
            "Set-ItemProperty -Path HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize -Name AppsUseLightTheme -Value 0;"
            "Set-ItemProperty -Path HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize -Name SystemUsesLightTheme -Value 0"
        ])
    else:
        subprocess.run([
            "powershell", "-Command",
            "Set-ItemProperty -Path HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize -Name AppsUseLightTheme -Value 1;"
            "Set-ItemProperty -Path HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize -Name SystemUsesLightTheme -Value 1"
        ])
    
    # Broadcast the theme change to all apps
    broadcast_theme_change()

# Example usage
if __name__ == "__main__":
    switch_theme(dark_mode=True)  # Set to dark mode
    time.sleep(2)  # Wait for a bit
    switch_theme(dark_mode=False)  # Set to light mode

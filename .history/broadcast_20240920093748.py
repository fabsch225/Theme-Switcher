import ctypes

HWND_BROADCAST = 0xFFFF
WM_SETTINGCHANGE = 0x001A

# Function to broadcast WM_SETTINGCHANGE message to all windows
def broadcast_theme_change():
    ctypes.windll.user32.SendMessageTimeoutW(HWND_BROADCAST, WM_SETTINGCHANGE, 0, 'ImmersiveColorSet', 0, 5000, None)

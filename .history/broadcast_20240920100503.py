import ctypes

HWND_BROADCAST = 0xFFFF
WM_SETTINGCHANGE = 0x001A
WM_THEMECHANGED = 0x031A  
WM_STYLECHANGED = 0x007D
WM_NCPAINT = 0x0085
WM_PAINT = 0x000F

# Function to broadcast WM_SETTINGCHANGE message to all windows
def broadcast_theme_change():
    ctypes.windll.user32.SendMessageTimeoutW(HWND_BROADCAST, WM_SETTINGCHANGE, 0, 'ImmersiveColorSet', 0, 5000, None)
    ctypes.windll.user32.SendMessageTimeoutW(HWND_BROADCAST, WM_THEMECHANGED, 0, 0, 0, 5000, None)
    ctypes.windll.user32.SendMessageTimeoutW(HWND_BROADCAST, WM_STYLECHANGED, 0, 0, 0, 5000, None)
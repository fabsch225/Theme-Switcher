import time
import platform_decider
from main import log
from main import detect_brightness_and_switch_theme

if __name__ == "__main__":
    os_id = platform_decider.get_os_id()
    log(f"Found {os_id} Environment")
    while True:
        detect_brightness_and_switch_theme(os_id)
        time.sleep(600)
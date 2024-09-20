import schedule
import time
import subprocess
from theme import detect_brightness_and_switch_theme  

schedule.every(10).minutes.do(detect_brightness_and_switch_theme)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)  # Sleep for a short time to avoid busy waiting

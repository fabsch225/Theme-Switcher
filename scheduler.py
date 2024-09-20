import time

from theme import detect_brightness_and_switch_theme  

if __name__ == "__main__":
    while True:
        detect_brightness_and_switch_theme()
        time.sleep(600)  

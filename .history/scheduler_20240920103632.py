import schedule
import time
import subprocess
from theme import detect_brightness_and_switch_theme  # Import the function directly

# Schedule the job to run every 10 minutes
schedule.every(10).minutes.do(run_theme_switcher)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)  # Sleep for a short time to avoid busy waiting

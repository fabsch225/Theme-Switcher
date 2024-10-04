import cv2
import numpy as np
import os
import time
import datetime
import platform_decider


def evaluate_natural_lighting_webcam(duration):
    # Start capturing video from the webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return 0.0  # Return a score of 0 for failure to open webcam

    scores = []
    start_time = time.time()

    while time.time() - start_time < duration:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        avg_color = np.mean(frame, axis=(0, 1))
        avg_gray = np.mean(gray_image)

        hist = cv2.calcHist([gray_image], [0], None, [256], [0, 256])
        total_pixels = gray_image.size
        bright_pixels = np.sum(hist[:120])
        darkness_ratio = bright_pixels / total_pixels

        lightness = (1 - darkness_ratio) * 5
        print("lightness : ", lightness)


        if avg_color[0] > avg_color[1] > avg_color[2]:
            color_temp_score = 1.5
        elif avg_color[0] < avg_color[1] and avg_color[1] > avg_color[2]:
            color_temp_score = 0.4
        else:
            color_temp_score = 1

        print("color_temp_score: ", color_temp_score)

        hist = cv2.calcHist([gray_image], [0], None, [256], [0, 256])
        hist /= hist.sum()
        histogram_std = np.std(hist)

        if histogram_std < 0.02:
            light_distribution_score = 0.6
        elif histogram_std < 0.05:
            light_distribution_score = 1
        else:
            light_distribution_score = 1.3

        print("light_distribution_score: ", light_distribution_score)

        edges = cv2.Canny(frame, 100, 200)
        edge_count = np.sum(edges)

        if edge_count < (frame.shape[0] * frame.shape[1]) * 0.1:
            shadow_score = 1.3
        elif edge_count < (frame.shape[0] * frame.shape[1]) * 0.2:
            shadow_score = 1
        else:
            shadow_score = 0.9

        print("shadow_score: ", shadow_score)

        final_score = (color_temp_score * light_distribution_score * shadow_score * lightness)
        scores.append(final_score)
        cv2.imshow("Webcam Feed", frame)
        cv2.waitKey(1)

    cap.release()
    cv2.destroyAllWindows()

    average_score = np.mean(scores)
    return average_score

def detect_brightness_and_switch_theme(os_id):
    brightnes_score = evaluate_natural_lighting_webcam(30)
    brightness_threshold = get_time_based_factor()
    log(f"Average Natural Lighting Score: {brightnes_score:.2f}, Daytime Factor is {brightness_threshold:.2f}")
    current_theme = platform_decider.get_theme(os_id)
    new_theme = ""
    if brightnes_score * brightness_threshold < 1:
        log(f"Switching to Dark Mode. {brightnes_score * brightness_threshold} < 1")
        new_theme = "dark"
    else:
        log(f"Switching to Light Mode. {brightnes_score * brightness_threshold} > 1")
        new_theme = "light"

    if new_theme != current_theme:
        platform_decider.set_theme(os_id, new_theme)

def get_time_based_factor():
    current_hour = datetime.datetime.now().hour
    log(f"Current hour is {current_hour}. The brightness threshold will be adjusted")
    if 6 <= current_hour < 12:  # Morning (6 AM to 12 PM)
        return 1.3
    elif 12 <= current_hour < 18:  # Afternoon (12 PM to 6 PM)
        return 1.1
    elif 18 <= current_hour < 21:  # Evening (6 PM to 9 PM)
        return 0.9
    else:  # Night (9 PM to 6 AM)
        return 0.6


def log(message):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    log_message = f"[{current_time}] {message}"
    print(log_message)
    log_directory = "./logs"
    log_filename = f"log_{current_date}.txt"

    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    log_filepath = os.path.join(log_directory, log_filename)
    with open(log_filepath, "a") as log_file:
        log_file.write(log_message + "\n")


if __name__ == "__main__":
    os_id = platform_decider.get_os_id()
    log(f"Found {os_id} Environment")
    detect_brightness_and_switch_theme(os_id)


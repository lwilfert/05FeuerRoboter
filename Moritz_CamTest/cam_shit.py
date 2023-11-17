from time import sleep

import cv2
import numpy as np
import requests
import pyrealsense2 as rs
from PIL import Image

URI = "http://127.0.0.1:5000"


def capture_frames():
    pipe = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 60)
    active = False

    i = 0

    while i < 10:
        if not active:
            pipe.start(config)
            active = True

        frames = pipe.wait_for_frames()
        color_frame = frames.get_color_frame()
        color_image = np.asanyarray(color_frame.get_data())

        img = Image.fromarray(cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB))

        img.save(f"/home/jens/Desktop/Moritz_CamTest/{i}.jpg", 'JPEG', quality=50)
        print("cool funktioniert")

        i += 1


def detect_line():
    pipe = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 60)
    active = False
    i = 0

    while i < 5:
        if not active:
            pipe.start(config)
            active = True

        frames = pipe.wait_for_frames()
        color_frame = frames.get_color_frame()
        color_image = np.asanyarray(color_frame.get_data())

        # img = Image.fromarray(cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB))

        # Convert the frame to HSV color space
        hsv = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)

        # Define lower and upper threshold for yellow in HSV
        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([40, 255, 255])

        # Create a mask to isolate the yellow regions
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

        # Apply morphological operations to clean up the mask
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) > 0:
            # Sort contours by area and select the largest one
            largest_contour = max(contours, key=cv2.contourArea)

            # Calculate the center of the yellow line
            M = cv2.moments(largest_contour)
            if M["m00"] != 0:  # "m00" = area
                cx = int(M["m10"] / M["m00"])  # "m10" = sum of all x coordinates
                cy = int(M["m01"] / M["m00"])  # "m01" = sum of all y coordinate

                # Determine whether the line is on the left, right, or center
                frame_center = color_image.shape[1] // 2
                if cx < frame_center - 40:
                    position = "left"
                    send_left_request()
                elif cx > frame_center + 40:
                    position = "right"
                    send_right_request()
                else:
                    position = "go"

                print(position)
                sleep(0.5)
                i += 1

                # Draw line in picture
                # cv2.drawContours(color_image, [largest_contour], -1, (0, 255, 0), 2)
                # cv2.putText(color_image, position, (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 255, 150), 2)

        # # Display the frame
        # cv2.imshow('Frame', img)
        #
        # if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' key to exit
        #     pipe.stop()
        #     cv2.destroyAllWindows()
        #     break
        stop_control_request()


def send_right_request():
    url = f"{URI}/right"
    body = {"value": 70}

    response = requests.post(url, json=body)
    print(response.text)

    # sleep(3)
    # stop_control_request()


def send_left_request():
    url = f"{URI}/right"
    body = {"value": 110}

    response = requests.post(url, json=body)
    print(response.text)


def stop_control_request():
    url = f"{URI}/stop"

    response = requests.post(url)
    print(response.text)


if __name__ == '__main__':
    # capture_frames()
    detect_line()

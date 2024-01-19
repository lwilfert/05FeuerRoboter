import time
from time import sleep
from turtle import pos

import cv2
import numpy as np
import pyrealsense2.pyrealsense2 as rs
from roboflow import Roboflow
import json
from PIL import Image

from katy_mainControl.abstract_component import Component, NotificationMessage


class CameraAnalyst(Component):
    def __init__(self, listener):
        super().__init__()
        self.listener = listener
        self.timeout_counter = 0
        api_key = ""
        with open("/home/jens/repo/Moritz_CamTest/config") as file:
            for i, line in enumerate(file):
                if i > 0:
                    break
                api_key = line.strip()
        rf = Roboflow(api_key=api_key)
        project = rf.workspace().project("car_stopping_points")
        self.model = project.version(3).model

    def get_target(self):
        return self.camera_stream

    def camera_stream(self):
        pipe = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 60)

        try:
            pipe.start(config)
            while True:
                frames = pipe.wait_for_frames()
                color_frame = frames.get_color_frame()
                color_image = np.asanyarray(color_frame.get_data())

                self.detect_line(color_image)
                self.detect_pattern(color_image)

                # img = Image.fromarray(cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB))
                # img.save(f"/home/jens/Desktop/Moritz_CamTest/{i}.jpg", 'JPEG', quality=50)

        except (ValueError, FileNotFoundError) as error:
            print(error)

        finally:
            pipe.stop()


    def detect_line(self, color_image):
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
            self.timeout_counter = 0

            # Sort contours by area and select the largest one
            largest_contour = max(contours, key=cv2.contourArea)

            # Calculate the center of the yellow line
            M = cv2.moments(largest_contour)
            if M["m00"] != 0:  # "m00" = area
                cx = int(M["m10"] / M["m00"])  # "m10" = sum of all x coordinates
                cy = int(M["m01"] / M["m00"])  # "m01" = sum of all y coordinate

                frame_width = color_image.shape[1]
                position_range = frame_width // 5  # Divide the frame width into 5 equal parts

                if cx < position_range:
                    value = 60
                    self.listener.notify_on_left(value)
                elif position_range <= cx < 2 * position_range:
                    value = 75
                    self.listener.notify_on_left(value)
                elif 2 * position_range <= cx < 3 * position_range:
                    self.listener.notify_on_center()
                elif 3 * position_range <= cx < 4 * position_range:
                    value = 105
                    self.listener.notify_on_right(value)
                else:
                    value = 120
                    self.listener.notify_on_right(value)

                time.sleep(0.1)
                # Draw line in picture
                # cv2.drawContours(color_image, [largest_contour], -1, (0, 255, 0), 2)
                # cv2.putText(color_image, position, (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 255, 150), 2)
        else:
            self.timeout_counter += 1
            print(self.timeout_counter)
            if self.timeout_counter == 15:
                self.listener.notify_on_forcestop()
                self.timeout_counter = 0
            time.sleep(0.1)

        # If this ever gets used again then refactor into camera_stream
        # # Display the frame
        # cv2.imshow('Frame', img)
        #
        # if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' key to exit
        #     pipe.stop()
        #     cv2.destroyAllWindows()
        #     break
        # send_stop_request()

    def detect_pattern(self, camera_image):
        output = self.model.predict(camera_image, confidence=95, overlap=30).json()
        print(f"json {output}")
        # class_names = [prediction["class"] for prediction in output["predictions"]]

        if output['predictions'] is not None and len(output['predictions']) > 0:
            self.listener.notify_on_destination_reached()


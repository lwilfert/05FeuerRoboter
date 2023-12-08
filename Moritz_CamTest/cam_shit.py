import time
from time import sleep
from turtle import pos

import cv2
import numpy as np
import pyrealsense2 as rs
from PIL import Image

from katy_mainControl.abstract_component import Component, NotificationMessage


class CameraAnalyst(Component):
    def __init__(self, listenerCallback):
        super().__init__()
        self.listenerCallback = listenerCallback

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
            cv2.destroyAllWindows()

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
            # Sort contours by area and select the largest one
            largest_contour = max(contours, key=cv2.contourArea)

            # Calculate the center of the yellow line
            M = cv2.moments(largest_contour)
            if M["m00"] != 0:  # "m00" = area
                cx = int(M["m10"] / M["m00"])  # "m10" = sum of all x coordinates
                cy = int(M["m01"] / M["m00"])  # "m01" = sum of all y coordinate

                # send_start_request()

                # Determine whether the line is on the left, right, or center
                frame_center = color_image.shape[1] // 2
                if cx < frame_center - 40:
                    position = NotificationMessage.LEFT
                    # send_left_request()
                elif cx > frame_center + 40:
                    position = NotificationMessage.RIGHT
                    # send_right_request()
                else:
                    position = NotificationMessage.CENTER
                    # send_left_request()

                self.listenerCallback(position)
                sleep(0.5)

                # Draw line in picture
                # cv2.drawContours(color_image, [largest_contour], -1, (0, 255, 0), 2)
                # cv2.putText(color_image, position, (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 255, 150), 2)

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
        pattern_image = cv2.imread("/home/jens/repo/Moritz_CamTest/flamme.jpg")

        # Check if the pattern image is loaded successfully
        if pattern_image is None:
            raise FileNotFoundError(f"Error: Unable to load the pattern image at '{pattern_image}'.")

        # Check if the input image and pattern image have compatible sizes
        if camera_image.shape[0] < pattern_image.shape[0] or camera_image.shape[1] < pattern_image.shape[1]:
            raise ValueError("Error: The input image is smaller than the pattern image.")

        # Convert images to grayscale
        input_gray = cv2.cvtColor(camera_image, cv2.COLOR_BGR2GRAY)
        pattern_gray = cv2.cvtColor(pattern_image, cv2.COLOR_BGR2GRAY)

        # Use template matching
        result = cv2.matchTemplate(input_gray, pattern_gray, cv2.TM_CCOEFF_NORMED)

        # Set a threshold to determine if the pattern is found
        threshold = 0.8
        locations = np.where(result >= threshold)

        # If any match is found, send destination reached message
        if locations[0].size > 0:
            self.listenerCallback(NotificationMessage.DESTINATION_REACHED)

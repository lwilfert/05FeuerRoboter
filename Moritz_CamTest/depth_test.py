from time import sleep
import cv2
import numpy as np
import requests
import pyrealsense2 as rs

ip = "http://192.168.171.91:5000"


def extract_frames_with_opencv():
    print("start of func")
    cap = cv2.VideoCapture(-1)
    i = 0

    while True:
        print("start of loop")
        ret, frame = cap.read()
        print(ret)
        if ret:
            if i > 10:
                break
            print("writing frame")
            cv2.imwrite('/home/jens/Desktop/Moritz_CamTest/opencv_frame_' + str(i) + '.jpg', frame)
            i += 1
        sleep(1)

    cap.release()
    cv2.destroyAllWindows()


def detect_line():
    cap = cv2.VideoCapture(-1)
    cap.release()
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    pipeline.start(config)

    while True:
        # Read frames from the RealSense camera
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()

        if not color_frame or not depth_frame:
            continue

        # Convert RealSense frames to NumPy arrays
        color_image = np.asanyarray(color_frame.get_data())
        depth_image = np.asanyarray(depth_frame.get_data())

        ret, frame = cap.read()

        if not ret:
            break

        # Convert the frame to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

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
                frame_center = frame.shape[1] // 2
                if cx < frame_center - 40:
                    position = "left"
                elif cx > frame_center + 40:
                    position = "right"
                else:
                    position = "go"

                print(position)
                # send_control_request(position)

                cv2.drawContours(frame, [largest_contour], -1, (0, 255, 0), 2)
                cv2.putText(frame, position, (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 255, 150), 2)

                # get depth
                depth_value = depth_image[cy, cx]
                distance_threshold = 50  # in millimeters

                if depth_value < distance_threshold:
                    print("Camera is closer than 5 cm to an object!")

        # Display the frame
        cv2.imshow('Frame', frame)

        if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' key to exit
            cap.release()
            cv2.destroyAllWindows()
            break


def send_control_request(request):
    url = f"{ip}/{request}"
    body = {"value": 0.2}

    response = requests.post(url, json=body)
    print(response.text)

    sleep(3)
    stop_control_request()


def stop_control_request():
    url = f"{ip}/stop"

    response = requests.post(url)
    print(response.text)


extract_frames_with_opencv()
print("Hallo")
# detect_line()

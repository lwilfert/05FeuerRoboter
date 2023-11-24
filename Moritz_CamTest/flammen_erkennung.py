import cv2
import numpy as np
import pyrealsense2 as rs

def detect_pattern(input_image, pattern_image_path):
    # Read the pattern image
    pattern_image = cv2.imread(pattern_image_path)

    # Check if the pattern image is loaded successfully
    if pattern_image is None:
        print(f"Error: Unable to load the pattern image at '{pattern_image_path}'.")
        return False

    # Check if the input image and pattern image have compatible sizes
    if input_image.shape[0] < pattern_image.shape[0] or input_image.shape[1] < pattern_image.shape[1]:
        print("Error: The input image is smaller than the pattern image.")
        return False

    # Convert images to grayscale
    input_gray = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    pattern_gray = cv2.cvtColor(pattern_image, cv2.COLOR_BGR2GRAY)

    # Use template matching
    result = cv2.matchTemplate(input_gray, pattern_gray, cv2.TM_CCOEFF_NORMED)

    # Set a threshold to determine if the pattern is found
    threshold = 0.8
    locations = np.where(result >= threshold)

    # If any match is found, return True
    if locations[0].size > 0:
        return True
    else:
        return False

def get_image_from_cam():
    pipe = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 60)
    active = False

    try:
        while True:
            if not active:
                pipe.start(config)
                active = True

            frames = pipe.wait_for_frames()
            color_frame = frames.get_color_frame()

            # Check if the color frame is available
            if not color_frame:
                print("Error: No color frame received.")
                continue

            color_image = np.asanyarray(color_frame.get_data())

            return color_image

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if active:
            pipe.stop()

# Example usage:
pattern_image_path = 'flamme.jpg'

while True:
    # Get an image from the camera
    input_image = get_image_from_cam()

    # show image
    cv2.imshow("test", input_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    if input_image is not None:
        # Detect the pattern in the input image
        result = detect_pattern(input_image, pattern_image_path)

        if result:
            print("Pattern detected in the input image.")
        else:
            print("Pattern not found in the input image.")
    else:
        print("Error: Unable to obtain an image from the camera.")

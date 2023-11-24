import cv2
import numpy as np
import pyrealsense2 as rs


def detect_pattern(camera_image, pattern_image):
    # Check if the pattern image is loaded successfully
    if pattern_image is None:
        print(f"Error: Unable to load the pattern image at '{pattern_image}'.")
        return False

    # Check if the input image and pattern image have compatible sizes
    if camera_image.shape[0] < pattern_image.shape[0] or camera_image.shape[1] < pattern_image.shape[1]:
        print("Error: The input image is smaller than the pattern image.")
        return False

    # Convert images to grayscale
    input_gray = cv2.cvtColor(camera_image, cv2.COLOR_BGR2GRAY)
    pattern_gray = cv2.cvtColor(pattern_image, cv2.COLOR_BGR2GRAY)

    # Use template matching
    result = cv2.matchTemplate(input_gray, pattern_gray, cv2.TM_CCOEFF_NORMED)

    # Set a threshold to determine if the pattern is found
    threshold = 0.8
    locations = np.where(result >= threshold)

    # If any match is found, return True
    return True if locations[0].size > 0 else False


def camera_stream():
    pipe = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 60)

    # Read the pattern image
    pattern_image = cv2.imread("flamme.jpg")

    try:
        pipe.start(config)
        while True:
            frames = pipe.wait_for_frames()
            color_frame = frames.get_color_frame()

            # Check if the color frame is available
            if not color_frame:
                print("Error: No color frame received.")
                break

            color_image = np.asanyarray(color_frame.get_data())

            cv2.imshow("Flamme da?", color_image)
            cv2.waitKey(3)

            # Detect the flamme
            result = detect_pattern(color_image, pattern_image)
            if result:
                print("Pattern detected in the input image.")
            else:
                print("Pattern not found in the input image.")
    finally:
        pipe.stop()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    camera_stream()

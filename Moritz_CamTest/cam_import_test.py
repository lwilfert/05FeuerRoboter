import pyrealsense2.pyrealsense2 as rs

def camera_stream():
    pipe = rs.pipeline()
    print("Hallo gescahfft")
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

camera_stream()

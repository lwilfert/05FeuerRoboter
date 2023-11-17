import os
import sys
import signal
import cv2
import numpy as np
import time
import pyrealsense2 as rs
from adafruit_servokit import ServoKit
from flask import Flask, request, jsonify, send_file
import io
import threading
import subprocess
from PIL import Image
import multiprocessing
from ultralytics import YOLO

print(sys.path)

app = Flask(__name__)

isForward = True
RIGHT = 65
FORWARD = 90
LEFT = 115
STOP = 0.0
current_speed = 0.0  # Neue globale Variable zur Speicherung der aktuellen Geschwindigkeit
BACKWARD = -0.3
kit = ServoKit(channels=16)
SERVO = 1
MOTOR = 0

current_angle = FORWARD  # Globale Variable zur Speicherung des aktuellen Winkels

kit.continuous_servo[MOTOR].throttle = current_speed
kit.servo[SERVO].angle = FORWARD
kit.continuous_servo[MOTOR].throttle = STOP

pipe = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 60)
active = False

# Load the YOLOv8 model
# model = YOLO('yolov8n.pt')

img_queue = multiprocessing.Queue(maxsize=1)

def cam_process(queue):
    global active
    while True:
        if not active:
            pipe.start(config)
            active = True

        frames = pipe.wait_for_frames()
        color_frame = frames.get_color_frame()
        color_image = np.asanyarray(color_frame.get_data())

        # Apply YOLOv8 to the frame
        # results = model.predict(source=color_image, verbose=False)

        # Draw the predictions on the frame
        # for result in results:
        #    for box in result.boxes.xyxy:
        #        x1, y1, x2, y2 = map(int, box[:4])
        #        cv2.rectangle(color_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        #        cv2.putText(color_image, f'{box[-1]:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

        img = Image.fromarray(cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB))
        
        if queue.empty():
            queue.put(img)

def exit():
    kit.continuous_servo[MOTOR].throttle = STOP
    kit.servo[SERVO].angle = FORWARD
    print('\nexiting program ', time.strftime('%d.%m.%Y %H:%M:%S', time.localtime()))
    cv2.destroyAllWindows()
    
def forward():
    kit.servo[SERVO].angle = FORWARD

def right(angle=None):
    global current_angle
    if angle is not None:
        current_angle = angle
    kit.servo[SERVO].angle = current_angle
    print(f"Turning Right with angle: {kit.servo[SERVO].angle}")

def left(angle=None):
    global current_angle
    if angle is not None:
        current_angle = angle
    kit.servo[SERVO].angle = current_angle
    print(f"Turning Left with angle: {kit.servo[SERVO].angle}")

def stop():
    kit.continuous_servo[MOTOR].throttle = STOP

def go(speed=None):
    global isForward, current_speed
    if speed is not None:
        current_speed = speed
    isForward = True
    kit.continuous_servo[MOTOR].throttle = current_speed
    print(f"Current Speed: {current_speed}")

def backward():
    global isForward
    if isForward:
        kit.continuous_servo[MOTOR].throttle = -0.1
        time.sleep(0.5)
        kit.continuous_servo[MOTOR].throttle = 0.0
        time.sleep(0.5)
        kit.continuous_servo[MOTOR].throttle = -0.1
        print("Backward +isForward=false")
        isForward = False
    else: 
        kit.continuous_servo[MOTOR].throttle = -0.1
        print("Backward")

@app.route('/right', methods=['POST'])
def api_right():
    data = request.get_json()
    angle = data.get('value', None)
    print("ANGLE RIGHT: ", angle)
    right(angle)
    return jsonify({'result': 'success'})

@app.route('/left', methods=['POST'])
def api_left():
    data = request.get_json()
    angle = data.get('value', None)
    print("ANGLE Left: ", angle)
    left(angle)
    return jsonify({'result': 'success'})

@app.route('/stop', methods=['POST'])
def api_stop():
    stop()
    return jsonify({'result': 'success'})
    
@app.route('/forward', methods=['POST'])
def api_forward():
    forward()
    return jsonify({'result': 'success'})

@app.route('/go', methods=['POST'])
def api_go():
    speed = request.get_json().get('value', current_speed)
    if speed is not None and isinstance(speed, (float, int)):
        print("Received Speed: ", speed)
        go(speed)
    else:
        print("Using last received speed.")
        go()
    return jsonify({'result': 'success'})

@app.route('/backward', methods=['POST'])
def api_backward():
    backward()
    return jsonify({'result': 'success'})

@app.route('/exit', methods=['POST'])
def api_exit():
    print("EXIT!!")
    exit()
    return jsonify({'result': 'success'})

@app.route('/cam', methods=['GET'])
def api_cam():
    img = img_queue.get()
    img_io = io.BytesIO()
    img.save(img_io, 'JPEG', quality=50)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')

if __name__ == '__main__':
    cam_process = multiprocessing.Process(target=cam_process, args=(img_queue,))
    cam_process.start()
    app.run(debug=False, host='0.0.0.0', port=5000)



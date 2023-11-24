import os
import sys
import cv2
import numpy as np
import time
import pyrealsense2 as rs
from adafruit_servokit import ServoKit
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import threading
import io
from PIL import Image

app = Flask(__name__)
CORS(app) 


# final variables with degree values for steering
RIGHT = 65
FORWARD = 90
LEFT = 115

# motor power - 1 = 100%, 0.04 is the minimum, less causes the motor to rotate irregularly, -0.01 is standstill - backward is unknown
STOP = 0.0# -0.01
GO = 0.25 #0.06
BACKWARD = -0.3

# instantiates the card for motor control - servo is connected to pin number 4 and motor 11
kit = ServoKit(channels=16)
SERVO = 3
MOTOR = 7 

# sets a minimum signal before starting the motor so that it can be calibrated and its power controlled
kit.continuous_servo[MOTOR].throttle = GO
kit.servo[SERVO].angle = FORWARD
kit.continuous_servo[MOTOR].throttle = STOP

# set up RealSense camera
pipe = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
active = False  # Flag to check if the stream is already active


def exit():
    kit.continuous_servo[MOTOR].throttle = STOP
    kit.servo[SERVO].angle = FORWARD
    print('\nexiting program ', time.strftime('%d.%m.%Y %H:%M:%S', time.localtime()))
    cv2.destroyAllWindows()

# Funktionen für die verschiedenen Befehle
def right(angle=RIGHT):
    kit.servo[SERVO].angle = angle

def forward():
    kit.servo[SERVO].angle = FORWARD

def left(angle=LEFT):
    kit.servo[SERVO].angle = angle

def stop():
    kit.continuous_servo[MOTOR].throttle = STOP

def go():
    kit.continuous_servo[MOTOR].throttle = GO

def backward():
    print("Prepare to go backwards")
    kit.continuous_servo[MOTOR].throttle = -1  
    time.sleep(1)  
    kit.continuous_servo[MOTOR].throttle = STOP  
    time.sleep(1)  
    kit.continuous_servo[MOTOR].throttle = BACKWARD  

def cam():
    global active  
    if not active:
        # Start the data stream from the camera
        pipe.start(config)
        active = True  
    frames = pipe.wait_for_frames()
    color_frame = frames.get_color_frame()

    # Convert the image into a numpy array and create a PIL image from it
    color_image = np.asanyarray(color_frame.get_data())
    img = Image.fromarray(cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB))
    return img

# REST-Endpunkte für die verschiedenen Befehle
@app.route('/right', methods=['POST'])
def api_right():
    angle = request.get_json().get('angle', RIGHT)
    print("ANGLE RIGHT: ", angle)
    right(angle)
    return jsonify({'result': 'success'})

@app.route('/forward', methods=['POST'])
def api_forward():
    forward()
    return jsonify({'result': 'success'})

@app.route('/left', methods=['POST'])
def api_left():
    angle = request.get_json().get('angle', LEFT)
    print("ANGLE Left: ", angle)
    left(angle)
    return jsonify({'result': 'success'})

@app.route('/stop', methods=['POST'])
def api_stop():
    stop()
    return jsonify({'result': 'success'})

@app.route('/go', methods=['POST'])
def api_go():
    go()
    return jsonify({'result': 'success'})

@app.route('/backward', methods=['POST'])
def api_backward():
    backward()
    return jsonify({'result': 'success'})

@app.route('/cam', methods=['GET'])
def api_cam():
    img = cam()
    img_io = io.BytesIO()
    img.save(img_io, 'JPEG', quality=25)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')

@app.route('/exit', methods=['POST'])
def api_exit():
    exit()
    return jsonify({'result': 'success'})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)

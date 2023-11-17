from time import sleep

import cv2
import numpy as np
import requests
import pyrealsense2 as rs
from PIL import Image

URI = "http://127.0.0.1:5000"


def send_right_request():
    url = f"{URI}/right"
    body = {"value": 80}

    response = requests.post(url, json=body)
    print(response.text)

    # sleep(3)
    # stop_control_request()


def send_left_request():
    url = f"{URI}/right"
    body = {"value": 100}

    response = requests.post(url, json=body)
    print(response.text)


def send_center_request():
    url = f"{URI}/right"
    body = {"value": 90}

    response = requests.post(url, json=body)
    print(response.text)


def send_start_request():
    url = f"{URI}/go"
    body = {"value": 0.12}

    response = requests.post(url, json=body)
    print(response.text)


def send_stop_request():
    url = f"{URI}/stop"

    response = requests.post(url)
    print(response.text)


send_start_request()
send_center_request()
sleep(2)
send_left_request()
sleep(2)
send_right_request()
sleep(2)
send_stop_request()

# send_right_request()
# send_center_request()
# send_stop_request()

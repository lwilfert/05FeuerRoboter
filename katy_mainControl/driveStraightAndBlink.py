import time
import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from api_adapter import ApiAdapter, TestApiAdapter
from luwiBlaulicht.blaulicht import BlueLightSwitch

api = ApiAdapter()
lights = BlueLightSwitch()

api.send_center_request()
api.send_go_request()
lights.start()
time.sleep(4)
api.send_stop_request()
lights.stop()

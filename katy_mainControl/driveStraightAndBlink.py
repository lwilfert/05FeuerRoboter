import time

from katy_mainControl.api_adapter import ApiAdapter
from luwiBlaulicht.blaulicht import BlueLightSwitch


api = ApiAdapter()
lights = BlueLightSwitch()

api.send_center_request()
api.send_go_request()
lights.start()
time.sleep(6)
api.send_stop_request()
lights.stop()

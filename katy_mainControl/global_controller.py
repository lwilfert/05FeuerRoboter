import sys
import os
import time
from pathlib import Path
from abstract_component import NotificationMessage

# add parent directory to import space, so we can keep directory structure
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from sirene.player import SoundPlayer
from luwiBlaulicht.blaulicht import BlueLightSwitch
from api_adapter import ApiAdapter
from Moritz_CamTest.cam_shit import CameraAnalyst
from luwiPowerSkript.waterpump import WaterPump

# TODO: only temporary to "compile"
from katy_intersectionsApi.intersection_guide import IntersectionGuide, Direction


class GlobalController:
    home_id = 0

    def __init__(self):
        self.api_adapter = ApiAdapter(ip="192.168.171.85", port=5000)
        self.sound_player = SoundPlayer("/home/jens/repo/sirene")
        self.sound_player.connect_bt()
        self.blue_light = BlueLightSwitch()
        print("blue light init finished")
        self.line_analyst = CameraAnalyst(self)
        self.intersection_guide = IntersectionGuide()
        self.pump_ctl = WaterPump()

        self.needs_privileges = False
        self.cached_message = None

    def notify_on_recognition(self, message: NotificationMessage):
        if message.value == NotificationMessage.FORCE_STOP.value:
            self.api_adapter.send_stop_request()

        if message.value != self.cached_message.value:
            self.cached_message = message
            if message.value == NotificationMessage.FORCE_STOP.value:
                self.api_adapter.send_stop_request()
            elif message.value == NotificationMessage.RIGHT.value:
                self.api_adapter.send_right_request()
            elif message.value == NotificationMessage.LEFT.value:
                self.api_adapter.send_left_request()
            elif message.value == NotificationMessage.CENTER.value:
                self.api_adapter.send_center_request()
            elif message.value == NotificationMessage.INTERSECTION.value:
                self.intersection_guide.find_intersection()
                direction = self.intersection_guide.get_current_direction()
                self.turn_after_intersection(direction)
            elif message.value == NotificationMessage.DESTINATION_REACHED.value:
                self.reach_destination()

    def turn_after_intersection(self, direction):
        # TODO: check if this is mechanically o.k.
        if direction == Direction.LEFT:
            self.api_adapter.send_left_request()
        elif direction == Direction.RIGHT:
            self.api_adapter.send_right_request()

    def reach_destination(self):
        self.api_adapter.send_stop_request()
        self.blue_light.stop()
        self.sound_player.stop()
        self.line_analyst.stop()

        self.pump_ctl.start_pumping_water()
        # simulate recognition of extinguished fire:
        time.sleep(3)
        self.pump_ctl.stop_pumping_water()

        self.u_turn()
        self.intersection_guide.reach_dest()
        self.set_destination_home()
        self.start_drive_to_destination(self.home_id)


    def u_turn(self):
        # TODO: implement mechanical u_turn
        print("not implemented yet")
        input("press any key to signalize you manually uturned the car.")

    def start_drive_to_destination(self, destination_id=1):
        if self.needs_privileges:
            self.blue_light.start()
            self.sound_player.start()
        self.line_analyst.start()
        print("goo")
        self.api_adapter.send_go_request()

    def set_destination_home(self):
        self.needs_privileges = False

    def set_destination_fire(self):
        self.needs_privileges = True


ctl = GlobalController()


def start(destination_id=1):
    ctl.set_destination_fire()
    ctl.start_drive_to_destination(destination_id)


start()


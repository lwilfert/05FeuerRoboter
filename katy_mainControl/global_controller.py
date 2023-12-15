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
        self.busy  =False
        self.api_adapter = ApiAdapter(ip="192.168.171.85", port=5000)
        self.sound_player = SoundPlayer("/home/jens/repo/sirene")
        self.sound_player.connect_bt()
        self.blue_light = BlueLightSwitch()
        self.line_analyst = CameraAnalyst(self)
        self.intersection_guide = IntersectionGuide()
        self.pump_ctl = WaterPump()

        self.needs_privileges = False
        self.cached_message = None
        self.cached_value = None

    # def notify_on_recognition(self, message: NotificationMessage, steeringValue: int=-1):
    #     if message.value == NotificationMessage.FORCE_STOP.value:
    #         self.api_adapter.send_stop_request()
    #
    #     if self.busy:
    #         return
    #
    #
    #     if self.cached_message is None or message.value != self.cached_message.value:
    #         self.cached_message = message
    #         if message.value == NotificationMessage.FORCE_STOP.value:
    #             self.api_adapter.send_stop_request()
    #         elif message.value == NotificationMessage.RIGHT.value:
    #             if steeringValue == -1:
    #                 self.api_adapter.send_right_request()
    #             else:
    #                 self.api_adapter.send_right_request(steeringValue)
    #         elif message.value == NotificationMessage.LEFT.value:
    #             if steeringValue == -1:
    #                 self.api_adapter.send_left_request()
    #             else:
    #                 self.api_adapter.send_left_request(steeringValue)
    #         elif message.value == NotificationMessage.CENTER.value:
    #             self.api_adapter.send_center_request()
    #         elif message.value == NotificationMessage.INTERSECTION.value:
    #             self.intersection_guide.find_intersection()
    #             direction = self.intersection_guide.get_current_direction()
    #             self.turn_after_intersection(direction)
    #         elif message.value == NotificationMessage.DESTINATION_REACHED.value:
    #             self.reach_destination()

    def notify_on_forcestop(self):
        self.api_adapter.send_stop_request()
        self.cached_message = NotificationMessage.FORCE_STOP
        print(f"stopped")

    def notify_on_center(self):
        if self.cached_message is None or self.cached_message != NotificationMessage.CENTER:
            self.api_adapter.send_center_request()
            print(f"center")
        self.cached_message = NotificationMessage.CENTER

    def notify_on_left(self, steering_value : int = -1):
        if self.cached_message is None or self.cached_message != NotificationMessage.LEFT or self.cached_value != steering_value:
            if steering_value == -1:
                self.api_adapter.send_left_request()
            else:
                self.api_adapter.send_left_request(steering_value)
                print(f"left {steering_value}")
        self.cached_message = NotificationMessage.LEFT
        self.cached_value = steering_value

    def notify_on_right(self, steering_value : int = -1):
        if self.cached_message is None or self.cached_message != NotificationMessage.RIGHT or self.cached_value != steering_value:
            if steering_value == -1:
                self.api_adapter.send_right_request()
            else:
                self.api_adapter.send_right_request(steering_value)
                print(f"right {steering_value}")
        self.cached_message = NotificationMessage.RIGHT
        self.cached_value = steering_value

    def notify_on_destination_reached(self):
        self.reach_destination()
        self.cached_message = NotificationMessage.DESTINATION_REACHED
        print(f"reached")

    def notify_on_intersection(self):
        self.intersection_guide.find_intersection()
        direction = self.intersection_guide.get_current_direction()
        self.turn_after_intersection(direction)


    def turn_after_intersection(self, direction):
        # TODO: check if this is mechanically o.k.
        if direction == Direction.LEFT:
            self.api_adapter.send_left_request()
        elif direction == Direction.RIGHT:
            self.api_adapter.send_right_request()

    def reach_destination(self):
        print("reach dest")
        self.api_adapter.send_stop_request()
        if self.needs_privileges:
            self.sound_player.stop()
            self.blue_light.stop()
            # self.line_analyst.stop()
            self.busy = True

            print("foo")
            self.pump_ctl.start_pumping_water()
            # simulate recognition of extinguished fire:
            print("exstinguishing...")
            time.sleep(3)
            print("fire dead")
            self.pump_ctl.stop_pumping_water()

            self.u_turn()
            self.intersection_guide.reach_dest()
            self.set_destination_home()
            self.busy = False
            self.start_drive_to_destination(self.home_id)
        else:
            print("reached fire station")


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


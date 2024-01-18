import os

on_path = "/home/jens/repo/luwiPowerSkript/powerWaterOn.sh"
off_path = "/home/jens/repo/luwiPowerSkript/powerWaterOff.sh"


class WaterPump:
    def start_pumping_water(self):
        print("arnie")
        os.popen(on_path)
        print("pumping")

    def stop_pumping_water(self):
        os.popen(off_path)
        print("stopped pumping")


# TODO: try if this works as component or why did i never include this?
# from katy_mainControl.abstract_component import Component
#
#
# class WaterPump(Component):
#     def get_target(self):
#         return self.start_pumping_water
#
#     def start_pumping_water(self):
#         os.popen(on_path)
#
#     def stop(self):
#         os.popen(off_path)
#         super.stop()

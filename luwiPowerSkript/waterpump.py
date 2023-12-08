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


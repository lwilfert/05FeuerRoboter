import os

on_path = "../luwiPowerSkript/powerWaterOn.sh"
off_path = "../luwiPowerSkript/powerWaterOff.sh"


class WaterPump:
    def start_pumping_water(self):
        os.popen(on_path)
        print("pumping")

    def stop_pumping_water(self):
        os.popen(off_path)
        print("stopped pumping")


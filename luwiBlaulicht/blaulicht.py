
import RPi.GPIO as GPIO
import time

from katy_mainControl.abstract_component import Component


class BlueLightSwitch(Component):
    def __init__(self):
        super().__init__()
        self.output_pin = 17
        self.output_pin2 = 18
        print(f"initialized blue light {self.output_pin}")

    def get_target(self):
        return self.blink_led

    def stop(self):
        GPIO.output(self.output_pin, GPIO.LOW)
        GPIO.output(self.output_pin2, GPIO.LOW)
        super().stop()

    def blink_led(self):
        GPIO.setmode(GPIO.BCM)  # BCM pin-numbering scheme from Raspberry Pi
        # set pin as an output pin with optional initial state of HIGH
        GPIO.setup(self.output_pin, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.output_pin2, GPIO.OUT, initial=GPIO.LOW)

        # print("Starting demo now! Press CTRL+C to exit")
        curr_value = GPIO.HIGH
        try:
            while True:
                time.sleep(1)
                # Toggle the output every second
                # print("Outputting {} to pin {}".format(curr_value, BlueLightSwitch.output_pin))
                GPIO.output(self.output_pin, curr_value)
                curr_value ^= GPIO.HIGH
                GPIO.output(self.output_pin2, curr_value)
        finally:
            GPIO.cleanup()



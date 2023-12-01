from playsound import playsound
import os

from katy_mainControl.abstract_component import Component


class SoundPlayer(Component):
    def __init__(self, path):
        self.base_path = path

    def get_target(self):
        return self.play_sound

    def play_sound(self):
        i = 0
        while True:
            if i >= 100000:
                i = 0
                SoundPlayer.connect_bt()
            playsound(f'{self.base_path}/martinshorn.mp3')
            i += 1

    def connect_bt(self):
        output = os.popen("sudo bluetoothctl info 12:0E:55:9D:45:2C | grep Connected |  awk -F ' ' '{print $2}'").read().strip()
        print(f'Speaker still connected: {output}')
        if 'yes' not in output:
           print('(re)connecting speaker')
           os.system(f'{self.base_path}/connectSpeaker.sh')

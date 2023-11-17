from playsound import playsound
import os
import time
from killable_thread import KillableThread


class Player:
    def __init__(self):
        self.thread: KillableThread = KillableThread(target=self.play_sound)
        # check bluetooth connection

    def start(self):
        self.thread.start()

    @staticmethod
    def play_sound():
        i = 0
        while True:
            if i >= 100000:
                i = 0
                Player.connectBT()
            playsound('./martinshorn.mp3')
            i += 1

    def stop(self):
        print("stopped")
        self.thread.kill()
        self.thread = KillableThread(target = self.play_sound)


    @staticmethod
    def connectBT():
        output = os.popen("sudo bluetoothctl info 12:0E:55:9D:45:2C | grep Connected |  awk -F ' ' '{print $2}'").read().strip()
        print(f'Speaker still connected: {output}')
        if 'yes' not in output:
           print('(re)connecting speaker')
           os.system('./connectSpeaker.sh')


def main():
    # in drive skript keep instance of Player
    player = Player()
    player.start()

    time.sleep(3)
    # after destination is reached:
    player.stop()
    time.sleep(3)
    player.start()
    time.sleep(3)
    player.stop()


if __name__ == "__main__":
    main()


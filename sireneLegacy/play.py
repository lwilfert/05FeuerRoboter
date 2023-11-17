from playsound import playsound
import os

# on boot start this script
path = 'config.jens'

def main():
    connectBT()
    print('main')
    i = 0
    while True:
        if i>=100000:
            i=0
            connectBT()
        play = False
        with open(path, 'r') as file:
            play = True if file.readline() == '0\n' else False
        # print(f'play:{play}')
        if play:
            playsound('./martinshorn.mp3')
        i+=1

def connectBT():
    output = os.popen("sudo bluetoothctl info 12:0E:55:9D:45:2C | grep Connected |  awk -F ' ' '{print $2}'").read().strip()
    print(f'Speaker still connected: {output}')
    if 'yes' not in output:
        print('(re)connecting speaker')
        os.system('./connectSpeaker.sh')

if __name__ == "__main__":
    main()

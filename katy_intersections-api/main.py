import time

import control
from threading import Thread


def main():
    while True:
        dest = input("Send signal [A|B|C|D] to start drive: ")
        if dest in control.route_map.keys():
            break
        print("unknown destination")
    car = control.Car()
    Thread(target=car.start_drive, args=(dest,)).start()

    # if plan size is 3, we need to see 1 intersection
    i = control.route_map.get(dest).__len__()
    while not i == 2:
        time.sleep(2)
        print('AI found intersection')
        car.find_intersection()
        i -= 1

    time.sleep(2.5)
    print('AI found reached destination')
    car.reach_dest()

    time.sleep(2)
    print('AI found extinguished fire')
    car.finish_extinguish()
    Thread(target=car.start_drive_home).start()

    i = control.route_map.get(dest).__len__()
    while not i == 2:
        time.sleep(2)
        print('AI found intersection')
        car.find_intersection()
        i -= 1

    time.sleep(2.5)
    print('AI found reached destination')
    car.reach_dest()

    # while True:
    #     event = input("find an intersection [I] or a destination [D]: ")
    #     if event == "I":
    #         t2 = Thread(target=car.find_intersection)
    #         t2.start()
    #     if event == "D":
    #         t3 = Thread(target=car.reach_dest)
    #         t3.start()
    #         break


if __name__ == "__main__":
    main()

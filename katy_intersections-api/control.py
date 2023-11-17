from enum import Enum
import time


# A --|-- B
#     |
# C --|-- D
#     |
#     H


class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    STRAIGHT = 3

    def get_counter_direction(self):
        if self == self.LEFT:
            return self.RIGHT
        elif self == self.RIGHT:
            return self.LEFT
        elif self == self.STRAIGHT:
            return self.STRAIGHT


route_map = {
    "A": [Direction.STRAIGHT, Direction.STRAIGHT, Direction.LEFT, Direction.STRAIGHT],
    "B": [Direction.STRAIGHT, Direction.STRAIGHT, Direction.RIGHT, Direction.STRAIGHT],
    "C": [Direction.STRAIGHT, Direction.LEFT, Direction.STRAIGHT],
    "D": [Direction.STRAIGHT, Direction.RIGHT, Direction.STRAIGHT],
}


class Car:
    def __init__(self):
        self.i = 0
        self.current_direction = Direction.STRAIGHT
        self.destination = ""
        self.route = []
        self.dest_reached = False

    def find_intersection(self):
        self.i += 1
        self.current_direction = self.route[self.i]
        self.mechanically_steer()

    def reach_dest(self):
        if not self.i == self.route.__len__() - 2:
            print("\tdestination seen but route not finished. Keep driving.")
        else:
            self.dest_reached = True
            self.mechanically_stop()

    def finish_extinguish(self):
        self.mechanically_stop_pump()

    def start_drive_home(self):
        self.mechanically_uturn()
        self.dest_reached = False
        self.start_drive("H")

    def set_destination(self, dest: str):
        self.i = 0
        self.destination = dest
        if self.destination == "H":
            self.route.reverse()
        else:
            self.route = route_map.get(self.destination)
        self.current_direction = self.route[0]

    def start_drive(self, dest: str):
        self.set_destination(dest)
        print(f'\tstarted drive to {dest}.')

        while not self.dest_reached:
            self.mechanically_drive()
        if not self.destination == "H":
            self.mechanically_pump()

    def mechanically_steer(self):
        print(f'\tsteer {self.current_direction.name}')

    def mechanically_drive(self):
        print('\tdriving')
        time.sleep(1.5)

    def mechanically_stop(self):
        print(f'\tstopped')

    def mechanically_pump(self):
        print(f'\tpump water')

    def mechanically_stop_pump(self):
        print(f'\tno longer pump water')

    def mechanically_uturn(self):
        print(f'\tuturned')

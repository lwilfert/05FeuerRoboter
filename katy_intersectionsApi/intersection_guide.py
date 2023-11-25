from enum import Enum


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
    0: [],
    1: [],
}


class IntersectionGuide:
    def __init__(self):
        self.i = 0
        self.current_direction = Direction.STRAIGHT
        self.destination = ""
        self.route = []
        self.dest_reached = False

    def find_intersection(self):
        self.current_direction = self.route[self.i]
        self.i += 1

    def reach_dest(self):
        if not self.i == self.route.__len__():
            print("\tdestination seen but route not finished. Keep driving.")
        self.dest_reached = True

    def start_drive_home(self):
        self.dest_reached = False
        self.start_drive(0)

    def set_destination(self, dest: int):
        self.i = 0
        self.destination = dest
        if self.destination == 0:
            self.route.reverse()
        else:
            self.route = route_map.get(self.destination)

    def start_drive(self, dest: int):
        self.set_destination(dest)

    def get_current_direction(self):
        return self.current_direction

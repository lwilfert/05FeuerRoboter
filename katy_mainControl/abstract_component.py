from abc import abstractmethod
from enum import Enum

from killable_thread import KillableThread
from threading import Thread


class NotificationMessage(Enum):
    LEFT = 0
    RIGHT = 1
    CENTER = 2
    INTERSECTION = 3
    DESTINATION_REACHED = 4
    FORCE_STOP = 5


class Component:
    def __init__(self):
        self.target = self.get_target()
        self.thread = KillableThread(target=self.target)

    @abstractmethod
    def get_target(self):
        ...

    def start(self):
        if not self.thread.is_alive():
            print(f"started")
            self.thread.start()
        else:
            print("still running")

    def stop(self):
        self.thread.kill()
        self.thread = KillableThread(target=self.target)
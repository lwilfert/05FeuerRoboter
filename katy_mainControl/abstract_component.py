from abc import abstractmethod

from katy_mainControl.killable_thread import KillableThread


class Component:
    def __init__(self):
        self.target = self.get_target()
        self.thread = KillableThread(target=self.target)

    @abstractmethod
    def get_target(self):
        ...

    def start(self):
        self.thread.start()

    def stop(self):
        self.thread.kill()
        self.thread = KillableThread(target=self.target)
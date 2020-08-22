from pynput.keyboard import Controller
keyboard = Controller()

from options.sequential.abstract.key import KeyBase


class Widget(KeyBase):
    def __init__(self, *args):
        super().__init__(*args)

    def run(self):
        keyboard.release(self.keyCache)

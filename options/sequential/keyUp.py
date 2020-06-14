from pynput.keyboard import Controller
keyboard = Controller()

from options.sequential.abstract.key import Key


class Widget(Key):
    def __init__(self, *args):
        super().__init__(*args)

    def run(self):
        keyboard.release(self.key.key)

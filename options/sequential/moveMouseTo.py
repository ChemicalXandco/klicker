import pyautogui

from options.sequential.abstract.mouseMove import MouseMoveBase


class Widget(MouseMoveBase):
    def __init__(self, *args):
        super().__init__(*args)

    def move(self, x, y):
        pyautogui.moveTo(x, y)

import pyautogui

from options.sequential.abstract.mouseButton import MouseButtonBase


class Widget(MouseButtonBase):
    def __init__(self, *args):
        super().__init__(*args)

    def run(self):
        pyautogui.mouseDown(button=self.buttonCache)

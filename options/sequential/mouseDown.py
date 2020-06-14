import pyautogui

from options.sequential.abstract.mouseButton import MouseButton


class Widget(MouseButton):
    def __init__(self, *args):
        super().__init__(*args)

    def run(self):
        pyautogui.mouseDown(button=self.choice.get())

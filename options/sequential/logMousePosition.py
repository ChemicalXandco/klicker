from tkinter import *
import pyautogui

from options.sequential import SequentialBase


class Widget(SequentialBase):
    def __init__(self, *args):
        super().__init__(*args)

    def run(self):
        pos = pyautogui.position()
        self.logger.info('Mouse cursor at ({}, {})'.format(pos[0], pos[1]))

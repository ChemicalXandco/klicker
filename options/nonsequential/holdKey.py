from tkinter import *

from pynput.keyboard import Controller
keyboard = Controller()

from options.nonsequential import NonsequentialBase
from options.utils import KeySelector


class Widget(NonsequentialBase):
    def __init__(self, *args):
        super().__init__(*args)

        self.labelOne = Label(self.parent, text='Hold')
        self.labelOne.grid(row=0, column=self.spacing)

        self.key = KeySelector(self.parent, self.root)
        self.key.grid(row=0, column=self.spacing+1)

    def start(self):
        self.keyCache = self.key.key
        keyboard.press(self.keyCache)

    def stop(self):
        keyboard.release(self.keyCache)

    def returnSettings(self):
        settings = {}
        settings['key'] = self.key.get()
        return settings

    def addSettings(self, settings):
        self.key.set(settings['key'])

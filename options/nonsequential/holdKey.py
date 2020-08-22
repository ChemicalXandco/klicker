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

    def registerSettings(self):
        self.keyCache = self.key.key

    def start(self):
        keyboard.press(self.keyCache)

    def stop(self):
        keyboard.release(self.keyCache)

    @property
    def settings(self):
        return { 'key': self.key.get() }

    @settings.setter
    def settings(self, settings):
        self.key.set(settings['key'])

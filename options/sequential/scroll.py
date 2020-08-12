from tkinter import *
import pyautogui

from options.sequential import SequentialBase
from options.numbers import Number


class Widget(SequentialBase):
    def __init__(self, *args):
        super().__init__(*args)

        self.labelOne = Label(self.parent, text='scroll mouse wheel')
        self.labelOne.grid(row=0, column=self.spacing, sticky=E)

        self.clicks = Number(self.parent, self.numbers)
        self.clicks.grid(row=0, column=self.spacing+1)

        self.labelTwo = Label(self.parent, text='"clicks"')
        self.labelTwo.grid(row=0, column=self.spacing+2, sticky=W)

    def run(self):
        pyautogui.scroll(self.clicks.parse())

    def returnSettings(self):
        return { 'clicks': self.clicks.get() }

    def addSettings(self, settings):
        self.clicks.set(settings['clicks'])

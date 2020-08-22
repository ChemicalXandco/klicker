from tkinter import *
from time import sleep

from options.sequential import SequentialBase
from options.numbers import Number


class Widget(SequentialBase):
    def __init__(self, *args):
        super().__init__(*args)

        self.labelOne = Label(self.parent, text='Wait')
        self.labelOne.grid(row=0, column=self.spacing, sticky=E)

        self.period = Number(self.parent, self.numbers)
        self.period.grid(row=0, column=self.spacing+1)

        self.labelTwo = Label(self.parent, text='seconds')
        self.labelTwo.grid(row=0, column=self.spacing+2, sticky=W)

    def registerSettings(self):
        self.period.registerSettings()

    def resetState(self):
        self.period.state.reset()

    def run(self):
        sleep(self.period.parse())

    @property
    def settings(self):
        return { 'period': self.period.get() }

    @settings.setter
    def settings(self, settings):
        self.period.set(settings['period'])

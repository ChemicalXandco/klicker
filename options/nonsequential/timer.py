from tkinter import *
import time

import options.sequential
from options.nonsequential import NonsequentialBase
from options.optionSelectors import OptionList
from options.numbers import Number


class Widget(NonsequentialBase):
    def __init__(self, *args):
        super().__init__(*args)

        self.frameOne = Frame(self.parent)
        self.frameOne.grid(row=0, column=self.spacing, sticky=W)

        self.labelOne = Label(self.frameOne, text='Every')
        self.labelOne.grid(row=0, column=0, sticky=E)

        self.seconds = Number(self.frameOne, self.numbers)
        self.seconds.grid(row=0, column=1)

        self.labelTwo = Label(self.frameOne, text='seconds')
        self.labelTwo.grid(row=0, column=2, sticky=W)

        self.options = LabelFrame(self.parent, text='do')
        self.options.grid(row=1, column=self.spacing, sticky=W)

        self.optionManger = OptionList(self.options, options.sequential, *self.args)

    def registerSettings(self):
        self.seconds.registerSettings()
        self.interval = self.seconds.parse()
        self.optionManger.registerSettings()

    def resetState(self):
        self.seconds.state.reset()
        self.optionManger.resetStates()

    def start(self):
        self.timer = time.time()
        self.addTime = 0

    def update(self):
        if time.time() >= self.timer + self.addTime:
            self.optionManger.runOptions()
            self.addTime += self.interval

    @property
    def settings(self):
        return {
            'options': self.optionManger.settings,
            'interval': self.seconds.get(),
        }

    @settings.setter
    def settings(self, settings):
        self.seconds.set(settings.pop('interval'))
        self.optionManger.destroyOptions()
        self.optionManger.settings = settings['options']

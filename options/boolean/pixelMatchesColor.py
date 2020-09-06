from tkinter import *
import pyautogui

from options.boolean import BooleanBase
from options.numbers import Number
from options.optionSelectors import SingleOption
import options.point


class Widget(BooleanBase):
    def __init__(self, *args):
        super().__init__(*args)

        self.point = SingleOption(self.parent, options.point, *self.args, row=0, column=self.spacing+1)

        self.labelThree = Label(self.parent, text='r:')
        self.labelThree.grid(row=1, column=self.spacing, sticky=E)

        self.r = Number(self.parent, self.numbers)
        self.r.grid(row=1, column=self.spacing+1)

        self.labelFour = Label(self.parent, text='g:')
        self.labelFour.grid(row=2, column=self.spacing, sticky=E)

        self.g = Number(self.parent, self.numbers)
        self.g.grid(row=2, column=self.spacing+1)

        self.labelFive = Label(self.parent, text='b:')
        self.labelFive.grid(row=3, column=self.spacing, sticky=E)

        self.b = Number(self.parent, self.numbers)
        self.b.grid(row=3, column=self.spacing+1)

    def registerSettings(self):
        self.point.registerSettings()
        for n in [self.r, self.g, self.b]:
            n.registerSettings()

    def resetState(self):
        self.point.resetState()
        for number in [self.r, self.g, self.b]:
            number.state.reset()

    def evaluate(self):
        try:
            return pyautogui.pixelMatchesColor(
                *self.point.getOption(),
                (
                    self.r.parse(),
                    self.g.parse(),
                    self.b.parse(),
                ),
            )
        except OSError as e:
            self.logger.error(e)

    @property
    def settings(self):
        return {
            'point': self.point.settings,
            'r': self.r.get(),
            'g': self.g.get(),
            'b': self.b.get(),
        }

    @settings.setter
    def settings(self, settings):
        self.point.settings = settings['point']
        self.r.set(settings['r'])
        self.g.set(settings['g'])
        self.b.set(settings['b'])

from tkinter import *
import pyautogui

from options.boolean import BooleanBase
from options.numbers import Number


class Widget(BooleanBase):
    def __init__(self, *args):
        super().__init__(*args)

        self.labelOne = Label(self.parent, text='x:')
        self.labelOne.grid(row=0, column=self.spacing, sticky=E)

        self.x = Number(self.parent, self.numbers)
        self.x.grid(row=0, column=self.spacing+1)

        self.labelTwo = Label(self.parent, text='y:')
        self.labelTwo.grid(row=1, column=self.spacing, sticky=E)

        self.y = Number(self.parent, self.numbers)
        self.y.grid(row=1, column=self.spacing+1)

        self.labelThree = Label(self.parent, text='r:')
        self.labelThree.grid(row=2, column=self.spacing, sticky=E)

        self.r = Number(self.parent, self.numbers)
        self.r.grid(row=2, column=self.spacing+1)

        self.labelFour = Label(self.parent, text='g:')
        self.labelFour.grid(row=3, column=self.spacing, sticky=E)

        self.g = Number(self.parent, self.numbers)
        self.g.grid(row=3, column=self.spacing+1)

        self.labelFive = Label(self.parent, text='b:')
        self.labelFive.grid(row=4, column=self.spacing, sticky=E)

        self.b = Number(self.parent, self.numbers)
        self.b.grid(row=4, column=self.spacing+1)

    def registerSettings(self):
        for n in [self.x, self.y, self.r, self.g, self.b]:
            n.registerSettings()

    def resetState(self):
        for number in [self.x, self.y, self.r, self.g, self.b]:
            number.state.reset()

    def evaluate(self):
        try:
            return pyautogui.pixelMatchesColor(
                self.x.parse(),
                self.y.parse(),
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
            'x': self.x.get(),
            'y': self.y.get(),
            'r': self.r.get(),
            'g': self.g.get(),
            'b': self.b.get(),
        }

    @settings.setter
    def settings(self, settings):
        self.x.set(settings['x'])
        self.y.set(settings['y'])
        self.r.set(settings['r'])
        self.g.set(settings['g'])
        self.b.set(settings['b'])

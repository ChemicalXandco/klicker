from tkinter import *

from options.sequential import SequentialBase
from options.numbers import Number


class MouseMoveBase(SequentialBase):
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

    def move(x, y):
        raise NotImplementedError

    def run(self):
        self.move(int(self.x.parse()), int(self.y.parse()))

    @property
    def settings(self):
        return {
            'x': self.x.get(),
            'y': self.y.get(),
        }

    @settings.setter
    def settings(self, settings):
        self.x.set(settings['x'])
        self.y.set(settings['y'])

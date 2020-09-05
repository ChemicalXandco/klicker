from tkinter import *

from options.sequential import SequentialBase
from options.optionSelectors import SingleOption
import options.point


class MouseMoveBase(SequentialBase):
    def __init__(self, *args):
        super().__init__(*args)

        self.point = SingleOption(self.parent, options.point, *self.args, row=0, column=0)

    def registerSettings(self):
        self.point.registerSettings()

    def resetState(self):
        self.point.resetState()

    def move(x, y):
        raise NotImplementedError

    def run(self):
        self.move(*self.point.getOption())

    @property
    def settings(self):
        return {
            'point': self.point.settings,
        }

    @settings.setter
    def settings(self, settings):
        self.point.settings = settings['settings']

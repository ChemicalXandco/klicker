from tkinter import *

from options.boolean import BooleanBase
from options.optionSelectors import SingleOption
import options.boolean


class Widget(BooleanBase):
    def __init__(self, *args):
        super().__init__(*args)

        self.a = SingleOption(self.parent, options.boolean, *self.args, column=self.spacing)

    def resetState(self):
        self.a.resetState()

    def evaluate(self):
        return not self.a.evaluateOption()

    @property
    def settings(self):
        return { 'a': self.a.settings }

    @settings.setter
    def settings(self, settings):
        self.a.settings = settings['a']

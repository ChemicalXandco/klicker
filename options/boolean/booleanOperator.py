from tkinter import *

import options.boolean
from options.boolean import BooleanBase
from options.optionSelectors import SingleOption


class Widget(BooleanBase):
    operators = ('AND', 'OR', 'XOR')
    def __init__(self, *args):
        super().__init__(*args)

        self.bool1 = SingleOption(self.parent, options.boolean, *self.args, column=self.spacing)

        self.selectedOption = StringVar(self.parent)
        self.selectedOption.set(self.operators[0])
        self.addOptions = OptionMenu(self.parent, self.selectedOption, *self.operators)
        self.addOptions.grid(row=0, column=self.spacing+1)

        self.bool2 = SingleOption(self.parent, options.boolean, *self.args, column=self.spacing+2)

    def evaluate(self):
        if self.selectedOption.get() == self.operators[0]:
            return self.bool1.evaluateOption() and self.bool2.evaluateOption()
        elif self.selectedOption.get() == self.operators[1]:
            return self.bool1.evaluateOption() or self.bool2.evaluateOption()
        elif self.selectedOption.get() == self.operators[2]:
            return self.bool1.evaluateOption() != self.bool2.evaluateOption()

    def returnSettings(self):
        settings = {}
        settings['a'] = self.bool1.getProfile()
        settings['b'] = self.bool2.getProfile()
        settings['operator'] = self.selectedOption.get()
        return settings

    def addSettings(self, settings):
        self.bool1.setProfile(settings['a'])
        self.bool2.setProfile(settings['b'])
        self.selectedOption.set(settings['operator'])

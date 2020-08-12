from tkinter import *

import options.boolean
from options.boolean.abstract.operator import BooleanOperatorBase
from options.optionSelectors import SingleOption


class Widget(BooleanOperatorBase):
    def __init__(self, *args):
        super().__init__(*args)

        self.a = SingleOption(self.parent, options.boolean, *self.args, column=self.spacing)
        self.b = SingleOption(self.parent, options.boolean, *self.args, column=self.spacing+2)

    def getResults(self, a=None, b=None):
        return {
            'AND': a and b,
            'OR': a or b,
            'NAND': not a and b,
            'NOR': not a or b,
            'XOR': a != b,
            'XNOR': not a != b,
        }

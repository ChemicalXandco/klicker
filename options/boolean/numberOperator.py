from tkinter import *

from options.boolean.abstract.operator import BooleanOperatorBase
from options.numbers import Number


class Widget(BooleanOperatorBase):
    def __init__(self, *args):
        super().__init__(*args)

        self.a = Number(self.parent, self.numbers)
        self.b = Number(self.parent, self.numbers)
        self.a.grid(row=0, column=self.spacing)
        self.b.grid(row=0, column=self.spacing+2)

    def getResults(self, a=0, b=0):
        return {
            'EQUALS': a == b,
            'NOT EQUALS': a != b,
            'GREATER THAN': a > b,
            'LESS THAN': a < b,
            'GREATER THAN OR EQUALS': a >= b,
            'LESS THAN OR EQUALS': a <= b,
        }

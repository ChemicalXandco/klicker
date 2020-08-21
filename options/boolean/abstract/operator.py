from tkinter import *

from options.boolean import BooleanBase


class BooleanOperatorBase(BooleanBase):
    def __init__(self, *args):
        super().__init__(*args)

        operators = list(self.getResults().keys())

        self.selectedOperator = StringVar(self.parent)
        self.selectedOperator.set(operators[0])
        self.selectOperator = OptionMenu(self.parent, self.selectedOperator, *operators)
        self.selectOperator.grid(row=0, column=self.spacing+1)

    def registerSettings(self):
        self.selectedOperatorCache = self.selectedOperator.get()
        for optionManager in [self.a, self.b]:
            optionManager.registerSettings()

    def getResults(self, a=None, b=None):
        """
        Get a dictionary representing names of operators and the outcome if they were applied.

        Args:
            a: The result of self.a.evaluateOption().
            b: The result of self.b.evaluateOption().
        Returns:
            dict: Keys are names of operators, values are booleans.
        """
        raise NotImplementedError()

    def evaluate(self):
        results = self.getResults(self.a.evaluateOption(), self.b.evaluateOption())
        return results[self.selectedOperatorCache]

    @property
    def settings(self):
        return {
            'a': self.a.settings,
            'b': self.b.settings,
            'operator': self.selectedOperator.get(),
        }

    @settings.setter
    def settings(self, settings):
        self.a.settings = settings['a']
        self.b.settings = settings['b']
        self.selectedOperator.set(settings['operator'])

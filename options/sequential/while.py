from tkinter import *

import options.boolean, options.sequential
from options.sequential import SequentialBase
from options.optionSelectors import SingleOption, OptionList


class Widget(SequentialBase):
    def __init__(self, *args):
        super().__init__(*args)

        self.frameOne = Frame(self.parent)
        self.frameOne.grid(row=0, column=self.spacing, sticky=W)

        self.labelOne = Label(self.frameOne, text='While')
        self.labelOne.grid(row=0, column=0, sticky=E)

        self.condition = SingleOption(self.frameOne, options.boolean, *self.args, row=0, column=1)

        self.options = LabelFrame(self.parent, text='do')
        self.options.grid(row=1, column=self.spacing, sticky=W)

        self.optionManger = OptionList(self.options, options.sequential, *self.args)

    def registerSettings(self):
        for optionManager in [self.condition, self.optionManger]:
            optionManager.registerSettings()

    def run(self):
        self.condition.resetState()
        self.optionManger.resetStates()
        while self.condition.evaluateOption():
            self.optionManger.runOptions()

    @property
    def settings(self):
        return {
            'options': self.optionManger.settings,
            'condition': self.condition.settings,
        }

    @settings.setter
    def settings(self, settings):
        self.optionManger.settings = settings['options']
        self.condition.settings = settings['condition']

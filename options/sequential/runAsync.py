from tkinter import *

import options.boolean, options.nonsequential
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

        self.asyncOptions = LabelFrame(self.parent, text='do')
        self.asyncOptions.grid(row=3, column=self.spacing, sticky=W)

        self.asyncOptionManger = OptionList(self.asyncOptions, options.nonsequential, *self.args)

    def registerSettings(self):
        for optionManager in [self.condition, self.asyncOptionManger]:
            optionManager.registerSettings()

    def run(self):
        self.asyncOptionManger.startOptions()
        while self.condition.evaluateOption():
            self.asyncOptionManger.updateOptions()
        self.asyncOptionManger.stopOptions()

    @property
    def settings(self):
        return {
            'options': self.asyncOptionManger.settings,
            'condition': self.condition.settings,
        }

    @settings.setter
    def settings(self, settings):
        self.asyncOptionManger.settings = settings['options']
        self.condition.settings = settings['condition']

from tkinter import *

import options.boolean, options.sequential
from options.sequential import SequentialBase
from options.optionSelectors import SingleOption, OptionList


class Widget(SequentialBase):
    def __init__(self, *args):
        super().__init__(*args)

        self.frameOne = Frame(self.parent)
        self.frameOne.grid(row=0, column=self.spacing, sticky=W)

        self.labelOne = Label(self.frameOne, text='If')
        self.labelOne.grid(row=0, column=0, sticky=E)

        self.condition = SingleOption(self.frameOne, options.boolean, *self.args, row=0, column=1)

        self.ifOptions = LabelFrame(self.parent, text='do')
        self.ifOptions.grid(row=1, column=self.spacing, sticky=W)

        self.ifOptionManger = OptionList(self.ifOptions, options.sequential, *self.args)

        self.labelTwo = Label(self.parent, text='Else')
        self.labelTwo.grid(row=2, column=self.spacing, sticky=W)

        self.elseOptions = LabelFrame(self.parent, text='do')
        self.elseOptions.grid(row=3, column=self.spacing, sticky=W)

        self.elseOptionManger = OptionList(self.elseOptions, options.sequential, *self.args)

    def run(self):
        if self.condition.evaluateOption():
            self.ifOptionManger.runOptions()
        else:
            self.elseOptionManger.runOptions()

    def returnSettings(self):
        settings = {}
        settings['if'] = self.ifOptionManger.getProfile()
        settings['else'] = self.elseOptionManger.getProfile()
        settings['condition'] = self.condition.getProfile()
        return settings

    def addSettings(self, settings):
        self.ifOptionManger.setProfile(settings['if'])
        self.elseOptionManger.setProfile(settings['else'])
        self.condition.setProfile(settings['condition'])

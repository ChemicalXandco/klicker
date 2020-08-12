from tkinter import *

import options.sequential
from options.nonsequential import NonsequentialBase
from options.optionSelectors import OptionList


class OnEventBase(NonsequentialBase):
    def __init__(self, *args):
        super().__init__(*args)

        self.frameOne = Frame(self.parent)
        self.frameOne.grid(row=0, column=self.spacing)

        self.optionManger = OptionList(self.frameOne, options.sequential, *self.args)

    def returnSettings(self):
        return { 'options': self.optionManger.getProfile() }

    def addSettings(self, settings):
        self.optionManger.destroyOptions()
        self.optionManger.setProfile(settings['options'])

from tkinter import *

import options.sequential
from options.nonsequential import NonsequentialBase
from options.optionSelectors import OptionList


class OnEvent(NonsequentialBase):
    def __init__(self, *args):
        super().__init__(*args)

        self.frameOne = Frame(self.parent)
        self.frameOne.grid(row=0, column=self.spacing)

        self.optionManger = OptionList(self.frameOne, options.sequential, *self.args)

    def returnSettings(self):
        settings = {}
        settings['options'] = self.optionManger.getProfile()
        return settings

    def addSettings(self, settings):
        self.optionManger.destroyOptions()
        self.optionManger.setProfile(settings['options'])

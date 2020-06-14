from tkinter import *

import gui
import options.sequential
from options.nonsequential import NonsequentialBase


class OnEvent(NonsequentialBase):
    def __init__(self, *args):
        super().__init__(*args)

        self.frameOne = Frame(self.parent)
        self.frameOne.grid(row=0, column=self.spacing)

        self.optionManger = gui.OptionManager(self.frameOne, options.sequential.optList, *self.args, sequential=True)

    def returnSettings(self):
        settings = self.optionManger.getProfile()
        return settings

    def addSettings(self, settings):
        self.optionManger.destroyOptions()
        self.optionManger.setProfile(settings)
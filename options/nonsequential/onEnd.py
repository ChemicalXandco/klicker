from tkinter import *
import time

import gui
import options.sequential
from options import Base


class Widget(Base):
    def __init__(self, *args):
        super().__init__(*args)

        self.frameOne = Frame(self.parent)
        self.frameOne.grid(row=0, column=self.spacing)

        self.optionManger = gui.OptionManager(self.frameOne, options.sequential.optList, *self.args, sequential=True)

    def start(self):
        return
        
    def stop(self):
        self.optionManger.runOptions()

    def update(self):
        return

    def returnSettings(self):
        settings = self.optionManger.getProfile()
        return settings

    def addSettings(self, settings):
        self.optionManger.destroyOptions()
        self.optionManger.setProfile(settings)

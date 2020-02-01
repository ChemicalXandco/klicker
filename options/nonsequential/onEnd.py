from tkinter import *
import time

import gui
import options.sequential

class Widget:
    def __init__(self, parent, spacing, logger):
        self.parent = parent

        self.frameOne = Frame(parent)
        self.frameOne.grid(row=0, column=spacing)

        self.optionManger = gui.OptionManager(self.frameOne, options.sequential.optList, logger, True, 50)

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

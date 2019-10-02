from tkinter import *
from time import sleep

from options.utils import DeactivateRequest


class Widget:
    def __init__(self, parent, spacing, logger):
        self.parent = parent

        self.labelOne = Label(parent, text='Stop execution of all options')
        self.labelOne.grid(row=0, column=spacing, sticky=E)

    def run(self):
        raise DeactivateRequest('Deactivated')

    def returnSettings(self):
        return {}

    def addSettings(self, settings):
        pass

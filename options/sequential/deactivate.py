from tkinter import *
from time import sleep

from options.utils import DeactivateRequest
from options import Base


class Widget(Base):
    def __init__(self, *args):
        super().__init__(*args)

        self.labelOne = Label(self.parent, text='Stop execution of all options')
        self.labelOne.grid(row=0, column=self.spacing, sticky=E)

    def run(self):
        raise DeactivateRequest('Deactivated')

    def returnSettings(self):
        return {}

    def addSettings(self, settings):
        pass

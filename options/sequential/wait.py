from tkinter import *
from time import sleep

from options import Base
from options.numbers import Number


class Widget(Base):
    def __init__(self, *args):
        super().__init__(*args)

        self.labelOne = Label(self.parent, text='Wait')
        self.labelOne.grid(row=0, column=self.spacing, sticky=E)

        self.period = Number(self.parent, self.numbers)
        self.period.grid(row=0, column=self.spacing+1)
    
        self.labelTwo = Label(self.parent, text='seconds')
        self.labelTwo.grid(row=0, column=self.spacing+2, sticky=W)

    def run(self):
        sleep(self.period.parse())

    def returnSettings(self):
        settings = {}
        settings['period'] = self.period.get()
        return settings

    def addSettings(self, settings):
        self.period.set(settings['period'])

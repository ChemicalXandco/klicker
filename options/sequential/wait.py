from tkinter import *
from time import sleep

from options import Base


class Widget(Base):
    def __init__(self, *args):
        super().__init__(*args)

        self.labelOne = Label(self.parent, text='Wait')
        self.labelOne.grid(row=0, column=self.spacing, sticky=E)

        self.period = Entry(self.parent, width=5)
        self.period.grid(row=0, column=self.spacing+1)
    
        self.labelTwo = Label(self.parent, text='seconds')
        self.labelTwo.grid(row=0, column=self.spacing+2, sticky=W)

    def run(self):
        period = float(self.period.get())
        
        sleep(period)
                

    def returnSettings(self):
        settings = {}
        settings['period'] = self.period.get()
        return settings

    def addSettings(self, settings):
        self.period.delete(0,END)
        self.period.insert(0, settings['period'])

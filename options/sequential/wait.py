from tkinter import *
from time import sleep


class Widget:
    def __init__(self, parent, spacing):
        self.parent = parent

        self.labelOne = Label(parent, text='Wait')
        self.labelOne.grid(row=0, column=spacing, sticky=E)

        self.period = Entry(parent, width=5)
        self.period.grid(row=0, column=spacing+1)
    
        self.labelTwo = Label(parent, text='seconds')
        self.labelTwo.grid(row=0, column=spacing+2, sticky=W)

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

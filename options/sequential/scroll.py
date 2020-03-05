from tkinter import *
import pyautogui

from options import Base


class Widget(Base):
    def __init__(self, *args):
        super().__init__(*args)

        self.labelOne = Label(self.parent, text='scroll mouse wheel')
        self.labelOne.grid(row=0, column=self.spacing, sticky=E)

        self.clicks = Entry(self.parent, width=5)
        self.clicks.grid(row=0, column=self.spacing+1)
    
        self.labelTwo = Label(self.parent, text='"clicks"')
        self.labelTwo.grid(row=0, column=self.spacing+2, sticky=W)

    def run(self):
        pyautogui.scroll(self.clicks.get())

    def returnSettings(self):
        settings = {}
        settings['clicks'] = self.clicks.get()
        return settings

    def addSettings(self, settings):
        self.clicks.delete(0,END)
        self.clicks.insert(0, settings['clicks'])

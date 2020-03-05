from tkinter import *
from time import sleep
import pyautogui

from options import Base


class Widget(Base):
    def __init__(self, *args):
        super().__init__(*args)

        self.choices = ['left', 'right']
        self.choice = StringVar(self.parent)
        self.choice.set(self.choices[0])
        self.mouseClick = OptionMenu(self.parent, self.choice, *self.choices)
        self.mouseClick.grid(row=0, column=self.spacing+1)

        self.labelTwo = Label(self.parent, text='mouse button down')
        self.labelTwo.grid(row=0, column=self.spacing+2, sticky=W)

    def run(self):
        pyautogui.mouseDown(button=self.choice.get()) 

    def returnSettings(self):
        settings = {}
        settings['mouseButton'] = self.choice.get()
        return settings

    def addSettings(self, settings):
        self.choice.set(settings['mouseButton'])

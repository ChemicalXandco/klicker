from tkinter import *
from time import sleep
import pyautogui

class Widget:
    def __init__(self, parent, spacing):
        self.parent = parent

        self.choices = ['left', 'right']
        self.choice = StringVar(parent)
        self.choice.set(self.choices[0])
        self.mouseClick = OptionMenu(parent, self.choice, *self.choices)
        self.mouseClick.grid(row=0, column=spacing+1)

        self.labelTwo = Label(parent, text='mouse button up')
        self.labelTwo.grid(row=0, column=spacing+2, sticky=W)

    def run(self):
        pyautogui.mouseUp(button=self.choice.get()) 

    def returnSettings(self):
        settings = {}
        settings['mouseButton'] = self.choice.get()
        return settings

    def addSettings(self, settings):
        self.choice.set(settings['mouseButton'])

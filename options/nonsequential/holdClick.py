from tkinter import *
import pyautogui

from options.nonsequential import NonsequentialBase


class Widget(NonsequentialBase):
    def __init__(self, *args):
        super().__init__(*args)

        self.labelOne = Label(self.parent, text='Hold')
        self.labelOne.grid(row=0, column=self.spacing)

        self.choices = ['left', 'right']
        self.choice = StringVar(self.parent)
        self.choice.set(self.choices[0])
        self.mouseClick = OptionMenu(self.parent, self.choice, *self.choices)
        self.mouseClick.grid(row=0, column=self.spacing+1)

        self.labelTwo = Label(self.parent, text='mouse button')
        self.labelTwo.grid(row=0, column=self.spacing+2)

    def start(self):
        self.currentButton = self.choice.get()
        pyautogui.mouseDown(button=self.currentButton)

    def stop(self):
        pyautogui.mouseUp(button=self.currentButton)

    def returnSettings(self):
        settings = {}
        settings['mouseButton'] = self.choice.get()
        return settings

    def addSettings(self, settings):
        self.choice.set(settings['mouseButton'])

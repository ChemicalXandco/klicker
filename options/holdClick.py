from tkinter import *
import pyautogui

class Widget:
    def __init__(self, parent, spacing):
        self.parent = parent

        self.labelOne = Label(parent, text='Hold')
        self.labelOne.grid(row=0, column=spacing)

        self.choices = ['left', 'right']
        self.choice = StringVar(parent)
        self.choice.set(self.choices[0])
        self.mouseClick = OptionMenu(parent, self.choice, *self.choices)
        self.mouseClick.grid(row=0, column=spacing+1)

        self.labelTwo = Label(parent, text='mouse button')
        self.labelTwo.grid(row=0, column=spacing+2)

    def start(self):
        self.currentButton = self.choice.get()
        pyautogui.mouseDown(button=self.currentButton)

    def stop(self):
        pyautogui.mouseUp(button=self.currentButton)

    def update(self):
        return

    def returnSettings(self):
        settings = {}
        settings['mouseButton'] = self.choice.get()
        return settings

    def addSettings(self, settings):
        self.choice.delete(0,END)
        self.choice.insert(0, settings['mouseButton'])

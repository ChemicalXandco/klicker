from tkinter import *
from time import sleep
import pyautogui

class Widget:
    def __init__(self, parent, spacing):
        self.parent = parent

        self.labelOne = Label(parent, text='click')
        self.labelOne.grid(row=0, column=spacing, sticky=E)

        self.choices = ['left', 'right']
        self.choice = StringVar(parent)
        self.choice.set(self.choices[0])
        self.mouseClick = OptionMenu(parent, self.choice, *self.choices)
        self.mouseClick.grid(row=0, column=spacing+1)

        self.labelTwo = Label(parent, text='mouse button')
        self.labelTwo.grid(row=0, column=spacing+2, sticky=W)

        self.labelThree = Label(parent, text='for')
        self.labelThree.grid(row=1, column=spacing, sticky=E)

        self.period = Entry(parent, width=5)
        self.period.grid(row=1, column=spacing+1)
    
        self.labelSix = Label(parent, text='seconds')
        self.labelSix.grid(row=1, column=spacing+2, sticky=W)

    def run(self):
        currentButton = self.choice.get()
        period = float(self.period.get())
        
        pyautogui.mouseDown(button=currentButton)
        sleep(period)
        pyautogui.mouseUp(button=currentButton) 
                

    def returnSettings(self):
        settings = {}
        settings['mouseButton'] = self.choice.get()
        settings['period'] = self.period.get()
        return settings

    def addSettings(self, settings):
        self.choice.set(settings['mouseButton'])
        self.period.delete(0,END)
        self.period.insert(0, settings['period'])

from tkinter import *
import time, pyautogui

class Widget:
    def __init__(self, parent, spacing):
        self.parent = parent

        self.labelOne = Label(parent, text='Every')
        self.labelOne.grid(row=0, column=spacing, sticky=E)

        self.seconds = Entry(parent, width=5)
        self.seconds.grid(row=0, column=spacing+1)

        self.labelTwo = Label(parent, text='seconds')
        self.labelTwo.grid(row=0, column=spacing+2, sticky=W)

        self.labelThree = Label(parent, text='click')
        self.labelThree.grid(row=1, column=spacing, sticky=E)

        self.choices = ['left', 'right']
        self.choice = StringVar(parent)
        self.choice.set(self.choices[0])
        self.mouseClick = OptionMenu(parent, self.choice, *self.choices)
        self.mouseClick.grid(row=1, column=spacing+1)

        self.labelFour = Label(parent, text='mouse button')
        self.labelFour.grid(row=1, column=spacing+2, sticky=W)

        self.labelFive = Label(parent, text='for')
        self.labelFive.grid(row=2, column=spacing, sticky=E)

        self.period = Entry(parent, width=5)
        self.period.grid(row=2, column=spacing+1)
    
        self.labelSix = Label(parent, text='seconds')
        self.labelSix.grid(row=2, column=spacing+2, sticky=W)

    def start(self):
        self.timer = time.time()
        self.interval = float(self.seconds.get())-0.1
        self.currentButton = self.choice.get()
        self.time = float(self.period.get())-0.1
        self.clicking = False

    def stop(self):
        return

    def update(self):
        timed = time.time()-self.timer
        if self.clicking:
            if timed >= self.time:
                pyautogui.mouseUp(button=self.currentButton)
                self.clicking = False
                self.timer = time.time()
        else:
            if timed >= self.interval:
                pyautogui.mouseDown(button=self.currentButton)
                self.clicking = True
                self.timer = time.time()

    def returnSettings(self):
        settings = {}
        settings['interval'] = self.seconds.get()
        settings['mouseButton'] = self.choice.get()
        settings['period'] = self.period.get()
        return settings

    def addSettings(self, settings):
        self.seconds.delete(0,END)
        self.seconds.insert(0, settings['interval'])
        self.choice.set(settings['mouseButton'])
        self.period.delete(0,END)
        self.period.insert(0, settings['period'])

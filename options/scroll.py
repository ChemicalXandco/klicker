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

        self.labelThree = Label(parent, text='scroll mouse wheel')
        self.labelThree.grid(row=1, column=spacing, sticky=E)

        self.clicks = Entry(parent, width=5)
        self.clicks.grid(row=1, column=spacing+1)
    
        self.labelFour = Label(parent, text='"clicks" (negative number will scroll down)')
        self.labelFour.grid(row=1, column=spacing+2, sticky=W)

    def start(self):
        self.timer = time.time()
        self.period = float(self.seconds.get())
        self.amount = int(self.clicks.get())

    def stop(self):
        return

    def update(self):
        timed = time.time()-self.timer
        if timed >= self.period:
            pyautogui.scroll(self.amount)
            self.timer = time.time()

    def returnSettings(self):
        settings = {}
        settings['time'] = self.seconds.get()
        settings['clicks'] = self.clicks.get()
        return settings

    def addSettings(self, settings):
        self.seconds.delete(0,END)
        self.seconds.insert(0, settings['time'])
        self.clicks.delete(0,END)
        self.clicks.insert(0, settings['clicks'])

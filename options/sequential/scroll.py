from tkinter import *
import pyautogui

class Widget:
    def __init__(self, parent, spacing):
        self.parent = parent

        self.labelOne = Label(parent, text='scroll mouse wheel')
        self.labelOne.grid(row=0, column=spacing, sticky=E)

        self.clicks = Entry(parent, width=5)
        self.clicks.grid(row=0, column=spacing+1)
    
        self.labelTwo = Label(parent, text='"clicks" (negative number will scroll down)')
        self.labelTwo.grid(row=0, column=spacing+2, sticky=W)

    def run(self):
        pyautogui.scroll(self.amount)
        self.timer = time.time()

    def returnSettings(self):
        settings = {}
        settings['clicks'] = self.clicks.get()
        return settings

    def addSettings(self, settings):
        self.clicks.delete(0,END)
        self.clicks.insert(0, settings['clicks'])

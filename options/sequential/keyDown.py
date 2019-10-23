from tkinter import *
import keyboard

class Widget:
    def __init__(self, parent, spacing, logger):
        self.parent = parent

        self.key = Entry(parent, width=5)
        self.key.grid(row=0, column=spacing)

        self.labelOne = Label(parent, text='key pressed')
        self.labelOne.grid(row=0, column=spacing+1, sticky=W)

    def run(self):
        keyboard.press(self.key.get()) 

    def returnSettings(self):
        settings = {}
        settings['key'] = self.key.get()
        return settings

    def addSettings(self, settings):
        self.key.delete(0,END)
        self.key.insert(0, settings['key'])

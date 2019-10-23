from tkinter import *
import keyboard

class Widget:
    def __init__(self, parent, spacing, logger):
        self.parent = parent

        self.labelOne = Label(parent, text='Hold')
        self.labelOne.grid(row=0, column=spacing)

        self.key = Entry(parent, width=5)
        self.key.grid(row=0, column=spacing+1)

    def start(self):
        keyboard.press(self.key.get())

    def stop(self):
        keyboard.release(self.key.get())

    def update(self):
        return

    def returnSettings(self):
        settings = {}
        settings['key'] = self.key.get()
        return settings

    def addSettings(self, settings):
        self.key.delete(0,END)
        self.key.insert(0, settings['key'])

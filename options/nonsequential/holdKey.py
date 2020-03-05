from tkinter import *
import keyboard

from options import Base


class Widget(Base):
    def __init__(self, *args):
        super().__init__(*args)

        self.labelOne = Label(self.parent, text='Hold')
        self.labelOne.grid(row=0, column=self.spacing)

        self.key = Entry(self.parent, width=5)
        self.key.grid(row=0, column=self.spacing+1)

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

from tkinter import *
import keyboard

from options import Base


class Widget(Base):
    def __init__(self, *args):
        super().__init__(*args)

        self.key = Entry(self.parent, width=5)
        self.key.grid(row=0, column=self.spacing)
        
        self.labelOne = Label(self.parent, text='key released')
        self.labelOne.grid(row=0, column=self.spacing+1, sticky=W)

    def run(self):
        keyboard.release(self.key.get())

    def returnSettings(self):
        settings = {}
        settings['key'] = self.key.get()
        return settings

    def addSettings(self, settings):
        self.key.delete(0,END)
        self.key.insert(0, settings['key'])

from tkinter import *
import pyautogui

from options import Base


class Widget(Base):
    def __init__(self, *args):
        super().__init__(*args)

        self.labelOne = Label(self.parent, text='move mouse by')
        self.labelOne.grid(row=0, column=self.spacing, columnspan=2)

        self.labelTwo = Label(self.parent, text='x:')
        self.labelTwo.grid(row=1, column=self.spacing, sticky=E)

        self.x = Entry(self.parent, width=5)
        self.x.grid(row=1, column=self.spacing+1)
    
        self.labelThree = Label(self.parent, text='y:')
        self.labelThree.grid(row=2, column=self.spacing, sticky=E)

        self.y = Entry(self.parent, width=5)
        self.y.grid(row=2, column=self.spacing+1)

    def run(self):
        pyautogui.moveRel(int(self.x.get()), int(self.y.get()))

    def returnSettings(self):
        settings = {}
        settings['x'] = self.x.get()
        settings['y'] = self.y.get()
        return settings

    def addSettings(self, settings):
        self.x.delete(0,END)
        self.x.insert(0, settings['x'])
        self.y.delete(0,END)
        self.y.insert(0, settings['y'])

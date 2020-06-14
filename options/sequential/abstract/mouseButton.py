from tkinter import *

from options.sequential import SequentialBase


class MouseButton(SequentialBase):
    def __init__(self, *args):
        super().__init__(*args)

        self.choices = ['left', 'right']
        self.choice = StringVar(self.parent)
        self.choice.set(self.choices[0])
        self.mouseClick = OptionMenu(self.parent, self.choice, *self.choices)
        self.mouseClick.grid(row=0, column=self.spacing)

    def returnSettings(self):
        settings = {}
        settings['mouseButton'] = self.choice.get()
        return settings

    def addSettings(self, settings):
        self.choice.set(settings['mouseButton'])
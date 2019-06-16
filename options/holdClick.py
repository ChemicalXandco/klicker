from tkinter import *

class Widget
    def __init__(self, parent, spacing):
        self.parent = parent

        self.labelOne = Label(parent, text='Hold')
        self.labelOne.grid(row=0, column=spacing)

        self.choices = ['left', 'right']
        self.choice = StringVar(parent)
        self.choice.set(self.choices[0])
        self.mouseClick = OptionMenu(parent, self.choice, *self.choices)
        self.mouseClick.grid(row=0, column=spacing+1)

        self.labelTwo = Label(parent, text='mouse button')
        self.labelTwo.grid(row=0, column=spacing+2)

from tkinter import *

class Widget:
    def __init__(self, parent, spacing):
        self.parent = parent

        self.labelOne = Label(parent, text='Every')
        self.labelOne.grid(row=0, column=spacing)

        self.seconds = Entry(parent, width=5)
        self.seconds.grid(row=0, column=spacing+1)

        self.labelTwo = Label(parent, text='seconds scroll mouse wheel')
        self.labelTwo.grid(row=0, column=spacing+2)

        self.clicks = Entry(parent, width=5)
        self.clicks.grid(row=0, column=spacing+3)
    
        self.labelThree = Label(parent, text='"clicks" (negative number will scroll down)')
        self.labelThree.grid(row=0, column=spacing+4)

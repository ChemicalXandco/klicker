from tkinter import *

from random import *
from random import uniform as randfloat
from math import *

import gui


class Number(Entry):
    def __init__(self, parent, numbers, **kwargs):
        if kwargs.get('width', 0) < 25:
            kwargs['width'] = 25
        super().__init__(parent, **kwargs)

        self.numbers = numbers

    def parse(self):
        string = self.get()

        for name,number in self.numbers.get().items():
            exec(name+'='+str(number))
        # using exec and eval allows math and random functions to be used, we are trusting the user not to input anything that would jeopardise the normal function of the software
        return eval(string)

    def set(self, value):
        self.delete(0, END)
        self.insert(0, value)


class Numbers(LabelFrame):
    def __init__(self, parent, text):
        super().__init__(parent, text=text)
        self.master = parent

        self.assigned = {}
        self.widgets = []

        self.addButton = Button(self, text='➕', command=self.add)
        self.addButton.grid(row=0, column=0)

        self.numbersGrid = Frame(self)
        self.numbersGrid.grid(row=1, column=0)

    def add(self):
        self.childWindow = Toplevel(self.master)
        self.childWindow.title('Name Number')
        gui.GUI.setWindowIcon(self.childWindow)
        self.childWindow.geometry('250x50')
        vcmd = (self.register(self.limitChar), '%i', '%S')
        self.newNumberName = Entry(self.childWindow, validate='key', validatecommand=vcmd)
        self.newNumberName.pack(fill=X, expand=YES)
        createButton = Button(self.childWindow, text="Create", command=self.assign)
        createButton.pack(fill=X, expand=YES)
    
    def limitChar(self, i, S):
        if i == '1': # if the index is 1 it means the string will be 2 characters long
            return False
        else:
            if S.isalpha(): # only alphabetic characters can be used
                return True
            else:
                return False

    def assign(self):
        self.assigned[self.newNumberName.get().lower()] = 0
        self.update()

    def get(self):
        return self.assigned

    def set(self, assigned):
        self.assigned = assigned
        self.update()

    def update(self):
        for l,e in self.widgets:
            l.destroy()
            e.destroy()
        self.widgets = []
        
        row = 0
        for k,v in self.assigned.items():
            self.widgets.append([Label(self.numbersGrid, text=k), Entry(self.numbersGrid)])
            self.widgets[row][0].grid(row=row, column=0)
            self.widgets[row][1].grid(row=row, column=1)

            self.widgets[row][1].insert(0, v)
            row += 1
            

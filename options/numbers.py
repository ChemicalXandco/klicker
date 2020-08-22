from tkinter import *
import time

from random import *
from random import uniform as randfloat
from math import *

import gui


class NumberState:
    def __init__(self):
        self.reset()

        self.stateNames = [
            'counter',
            'timer',
        ]

    def reset(self):
        self._counter = 0
        self._startTime = time.time()

        self._cache = None

    def counter(self):
        value = self._counter
        self._counter += 1
        return value

    def timer(self):
        return time.time() - self._startTime

    def cache(self, number):
        if self._cache is None:
            self._cache = number
        return self._cache

    @property
    def states(self):
        return { i: getattr(self, i)() for i in self.stateNames }


class Number(Entry):
    def __init__(self, parent, numbers, **kwargs):
        if kwargs.get('width', 0) < 25:
            kwargs['width'] = 25
        super().__init__(parent, **kwargs)

        self.numbers = numbers

        self.state = NumberState()

    def registerSettings(self):
        self.cache = self.get()

    def parse(self):
        # setup variables
        for state, value in self.state.states.items():
            exec(state+'='+str(value))
        for name, number in self.numbers.get().items():
            exec(name+'='+str(number))

        # setup functions
        cache = self.state.cache

        # using eval allows math and random functions to be used, we are trusting the user not to input anything that would jeopardise the normal function of the software
        return eval(self.cache)

    def evaluateOption(self): # for boolean/abstract/operator.py
        return self.parse()

    def set(self, value):
        self.delete(0, END)
        self.insert(0, value)

    @property
    def settings(self):
        return { 'text': self.get() }

    @settings.setter
    def settings(self, settings):
        self.set(settings['text'])


class Numbers(LabelFrame):
    def __init__(self, parent, text):
        super().__init__(parent, text=text)
        self.master = parent

        self.assigned = {}
        self.widgets = []

        self.numbersOptionsFrame = Frame(self)
        self.numbersOptionsFrame.pack()

        self.addButton = Button(self.numbersOptionsFrame, text='➕', command=self.add)
        self.addButton.grid(row=0, column=0)

        self.numbersFrame = gui.ScrollFrame(self, (400, 100))
        self.numbersFrame.pack(fill=BOTH, expand=YES)
        self.numbersGrid = self.numbersFrame.viewPort

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
        self.childWindow.destroy()
        self.update()

    def get(self):
        return self.assigned

    def set(self, assigned):
        self.assigned = assigned
        self.update()

    def remove(self, letter):
        del self.assigned[letter]
        self.update()

    def update(self):
        for b,l,e in self.widgets:
            b.destroy()
            l.destroy()
            e.destroy()
        self.widgets = []

        row = 0
        for k,v in self.assigned.items():
            self.widgets.append(
                (
                    Button(self.numbersGrid, text='❌', command=lambda k=k: self.remove(k)),
                    Label(self.numbersGrid, text=k),
                    Entry(self.numbersGrid)
                )
            )
            self.widgets[row][0].grid(row=row, column=0)
            self.widgets[row][1].grid(row=row, column=1)
            self.widgets[row][2].grid(row=row, column=2)

            self.widgets[row][2].insert(0, v)
            row += 1

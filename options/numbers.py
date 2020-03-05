from tkinter import *

import gui


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
        gui.GUI.setWindowIcon(self, self.childWindow)
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
        self.assigned[self.newNumberName.get()] = 0
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
            

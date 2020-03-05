from tkinter import *


class Numbers(LabelFrame):
    def __init__(self, parent, text):
        super().__init__(parent, text=text)

        self.assigned = {}
        self.widgets = []

        self.add = Button(self, text='➕', command=self.assign)
        self.add.grid(row=0, column=0)

        self.numbersGrid = Frame(self)
        self.numbersGrid.grid(row=1, column=0)

    def assign(self):
        self.assigned = {'ayyy':0}
        self.update()

    def get(self):
        return self.assigned

    def set(self, assigned):
        self.assigned = assigned
        self.update()

    def update(self):
        row = 0
        for k,v in self.assigned.items():
            self.widgets.append([Label(self.numbersGrid, text=k), Entry(self.numbersGrid)])
            self.widgets[row][0].grid(row=row, column=0)
            self.widgets[row][1].grid(row=row, column=1)
            row += 1
            

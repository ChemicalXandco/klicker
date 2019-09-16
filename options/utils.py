from tkinter import *
from tkinter.filedialog import askopenfilename


class FileSelector(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.button = Button(self, text='Select File', command=self.getFilename)
        self.button.grid(row=0, column=0)
        self.path = Entry(self, width=35)
        self.path.grid(row=0, column=1)
        
    def getFilename(self):
        filename = askopenfilename()
        self.path.delete(0,END)
        self.path.insert(0, filename)

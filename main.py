import pyautogui
import keyboard
from tkinter import *

class GUI:
    def __init__(self, master):
        self.master = master
        master.title('Simple Clicker')

        self.label = Label(master, text='Options')
        self.label.pack()

        self.key1 = Entry(master)
        self.key1.pack()

        self.key2 = Entry(master)
        self.key2.pack()

        self.choices = ['left', 'right', 'both']
        self.choice = StringVar(master)
        self.choice.set(self.choices[0])
        self.mouseClick = OptionMenu(master, self.choice, *self.choices)
        self.mouseClick.pack()

        self.refreshButton = Button(master, text='Refresh', command=self.readSetting)
        self.refreshButton.pack()

        self.saveButton = Button(master, text='Save', command=self.writeSetting)
        self.saveButton.pack()

        self.closeButton = Button(master, text='Close', command=master.quit)
        self.closeButton.pack()

    def readSetting(self):
        f = open('config.ini', 'r')
        self.key1.delete(0, END)
        self.key2.delete(0, END)
        self.key1.insert(0, f.readline().strip())
        self.key2.insert(0, f.readline().strip())
        self.choice.set(f.readline().strip())
        f.close

    def writeSetting(self):
        f = open('config.ini', 'w')
        f.write(self.key1.get()+'\n')
        f.write(self.key2.get()+'\n')
        f.write(self.choice.get())
        f.close()

root = Tk()
gui = GUI(root)
root.mainloop()

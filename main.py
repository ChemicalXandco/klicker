import pyautogui
import keyboard
from tkinter import *

class GUI:
    def __init__(self, master):
        self.master = master
        master.title('Simple Clicker')

        self.label = Label(master, text='Options')
        self.label.pack()

        self.hotkey = Entry(master)
        self.hotkey.pack()

        self.choices = ['left', 'right', 'both']
        self.choice = StringVar(master)
        self.choice.set(self.choices[0])
        self.mouseClick = OptionMenu(master, self.choice, *self.choices)
        self.mouseClick.pack()

        self.refreshButton = Button(master, text='Refresh', command=self.readSetting)
        self.refreshButton.pack()

        self.saveButton = Button(master, text='Save', command=self.writeSetting)
        self.saveButton.pack()

        self.error = Label(master, text='', fg='#ff0000')
        self.error.pack()

        self.readSetting()

    def readSetting(self):
        f = open('config.ini', 'r')
        self.hotkey.delete(0, END)
        self.hotkey.insert(0, f.readline().strip())
        self.choice.set(f.readline().strip())
        f.close

    def writeSetting(self):
        f = open('config.ini', 'w')
        f.write(self.hotkey.get()+'\n')
        f.write(self.choice.get())
        f.close()

root = Tk()
gui = GUI(root)
try:
    while True:
        root.update_idletasks()
        root.update()
    
except Exception as e:
    gui.error.config(text=e)
    

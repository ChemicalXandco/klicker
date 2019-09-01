from tkinter import *
import pyautogui

class Widget:
    def __init__(self, parent, spacing):
        self.parent = parent

        self.labelOne = Label(parent, text='Locate image')
        self.labelOne.grid(row=0, column=spacing, sticky=E)

        self.img = Entry(parent, width=20)
        self.img.grid(row=0, column=spacing+1)
    
        self.labelTwo = Label(parent, text='on screen and move cursor')
        self.labelTwo.grid(row=0, column=spacing+2, sticky=W)

    def run(self):
        location = pyautogui.locateCenterOnScreen(self.img.get())
        if location != None:
            pyautogui.moveTo(location[0], location[1])
        else:
            raise RuntimeError('Could not locate the given image on the screen')

    def returnSettings(self):
        settings = {}
        settings['imgPath'] = self.img.get()
        return settings

    def addSettings(self, settings):
        self.img.delete(0,END)
        self.img.insert(0, settings['imgPath'])

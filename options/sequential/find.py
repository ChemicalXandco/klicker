from tkinter import *
from options.utils import FileSelector
import pyautogui

class Widget:
    def __init__(self, parent, spacing, logger):
        self.parent = parent

        self.labelOne = Label(parent, text='Locate image')
        self.labelOne.grid(row=0, column=spacing)

        self.img = FileSelector(parent)
        self.img.grid(row=1, column=spacing)
    
        self.labelTwo = Label(parent, text='on screen and move cursor')
        self.labelTwo.grid(row=2, column=spacing)

    def run(self):
        location = pyautogui.locateCenterOnScreen(self.img.path.get())
        if location != None:
            pyautogui.moveTo(location[0], location[1])
        else:
            raise RuntimeError('Could not locate the given image on the screen')

    def returnSettings(self):
        settings = {}
        settings['imgPath'] = self.img.path.get()
        return settings

    def addSettings(self, settings):
        self.img.path.delete(0,END)
        self.img.path.insert(0, settings['imgPath'])

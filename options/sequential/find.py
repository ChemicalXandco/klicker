from tkinter import *
from options.utils import FileSelector
import pyautogui

from options.sequential import SequentialBase


class Widget(SequentialBase):
    def __init__(self, *args):
        super().__init__(*args)

        self.labelOne = Label(self.parent, text='Locate image')
        self.labelOne.grid(row=0, column=self.spacing)

        self.img = FileSelector(self.parent)
        self.img.grid(row=1, column=self.spacing)

        self.labelTwo = Label(self.parent, text='on screen and move cursor')
        self.labelTwo.grid(row=2, column=self.spacing)

    def registerSettings(self):
        self.imgPathCache = self.img.path.get()

    def run(self):
        imgPath = self.imgPathCache
        location = pyautogui.locateCenterOnScreen(imgPath)
        if location != None:
            self.logger.debug('Found {} at ({}, {})'.format(imgPath, location[0], location[1]))
            pyautogui.moveTo(location[0], location[1])
        else:
            raise RuntimeError('Could not locate the given image on the screen')

    @property
    def settings(self):
        return { 'imgPath': self.img.path.get() }

    @settings.setter
    def settings(self, settings):
        self.img.path.delete(0,END)
        self.img.path.insert(0, settings['imgPath'])

from tkinter import *
import pyautogui

from options.point import PointBase
from options.utils import FileSelector


class Widget(PointBase):
    def __init__(self, *args):
        super().__init__(*args)

        self.labelOne = Label(self.parent, text='Locate')
        self.labelOne.grid(row=0, column=self.spacing)

        self.img = FileSelector(self.parent)
        self.img.grid(row=1, column=self.spacing)

    def registerSettings(self):
        self.imgPathCache = self.img.path.get()

    def get(self):
        location = pyautogui.locateCenterOnScreen(self.imgPathCache)
        if location != None:
            self.logger.debug('Found {} at ({}, {})'.format(self.imgPathCache, location[0], location[1]))
            return location
        else:
            raise RuntimeError('Could not locate the given image on the screen')

    @property
    def settings(self):
        return { 'imgPath': self.img.path.get() }

    @settings.setter
    def settings(self, settings):
        self.img.path.delete(0,END)
        self.img.path.insert(0, settings['imgPath'])

from tkinter import *
import pyautogui

from options.boolean import BooleanBase
from options.utils import FileSelector


class Widget(BooleanBase):
    def __init__(self, *args):
        super().__init__(*args)

        self.labelOne = Label(self.parent, text='Image')
        self.labelOne.grid(row=0, column=self.spacing)

        self.img = FileSelector(self.parent)
        self.img.grid(row=1, column=self.spacing)

    def registerSettings(self):
        self.imgPathCache = self.img.path.get()

    def evaluate(self):
        try:
            location = pyautogui.locateOnScreen(self.imgPathCache)
            return location
        except pyautogui.ImageNotFoundException:
            return False

    @property
    def settings(self):
        return { 'imgPath': self.img.path.get() }

    @settings.setter
    def settings(self, settings):
        self.img.path.delete(0,END)
        self.img.path.insert(0, settings['imgPath'])

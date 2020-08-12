from tkinter import *

from pynput.keyboard import Controller
keyboard = Controller()

from options.sequential import SequentialBase


class Widget(SequentialBase):
    def __init__(self, *args):
        super().__init__(*args)

        self.text = Entry(self.parent, width=20)
        self.text.grid(row=0, column=self.spacing)

    def run(self):
        keyboard.type(self.text.get())

    @property
    def settings(self):
        return { 'text': self.text.get() }

    @settings.setter
    def settings(self, settings):
        self.text.delete(0,END)
        self.text.insert(0, settings['text'])
from tkinter import *

from options.sequential import SequentialBase


class Widget(SequentialBase):
    def __init__(self, *args):
        super().__init__(*args)

        self.text = Entry(self.parent, width=20)
        self.text.grid(row=0, column=self.spacing)

    def registerSettings(self):
        self.textCache = self.text.get()

    def run(self):
        self.logger.info(self.textCache)

    @property
    def settings(self):
        return { 'text': self.text.get() }

    @settings.setter
    def settings(self, settings):
        self.text.delete(0,END)
        self.text.insert(0, settings['text'])

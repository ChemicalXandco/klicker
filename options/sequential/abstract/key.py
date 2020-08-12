from tkinter import *

from options.sequential import SequentialBase
from options.utils import KeySelector


class KeyBase(SequentialBase):
    def __init__(self, *args):
        super().__init__(*args)

        self.key = KeySelector(self.parent, self.root)
        self.key.grid(row=0, column=self.spacing)

    def returnSettings(self):
        return { 'key': self.key.get() }

    def addSettings(self, settings):
        self.key.set(settings['key'])
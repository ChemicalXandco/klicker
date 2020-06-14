from tkinter import *

from options.sequential import SequentialBase
from options.utils import KeySelector


class Key(SequentialBase):
    def __init__(self, *args):
        super().__init__(*args)

        self.key = KeySelector(self.parent, self.root)
        self.key.grid(row=0, column=self.spacing) 

    def returnSettings(self):
        settings = {}
        settings['key'] = self.key.get()
        return settings

    def addSettings(self, settings):
        self.key.set(settings['key'])
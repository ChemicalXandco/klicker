from tkinter import *
import time

import gui
import options.sequential
from options.nonsequential import NonsequentialBase
from options.numbers import Number


class Widget(NonsequentialBase):
    def __init__(self, *args):
        super().__init__(*args)

        self.frameOne = Frame(self.parent)
        self.frameOne.grid(row=0, column=self.spacing, sticky=W)

        self.labelOne = Label(self.frameOne, text='After')
        self.labelOne.grid(row=0, column=0, sticky=E)

        self.seconds = Number(self.frameOne, self.numbers)
        self.seconds.grid(row=0, column=1)

        self.labelTwo = Label(self.frameOne, text='seconds')
        self.labelTwo.grid(row=0, column=2, sticky=W)

        self.options = LabelFrame(self.parent, text='do')
        self.options.grid(row=1, column=self.spacing, sticky=W)

        self.optionManger = gui.OptionManager(self.options, options.sequential.optList, *self.args, sequential=True)

    def start(self):
        self.timer = time.time()
        self.waitTime = self.seconds.parse()
        self.hasRan = False

    def update(self):
        if not self.hasRan:
            timed = time.time()-self.timer
            if timed >= self.waitTime:
                self.hasRan = True
                self.optionManger.runOptions()

    def returnSettings(self):
        settings = self.optionManger.getProfile()
        settings['waitTime'] = self.seconds.get()
        return settings

    def addSettings(self, settings):
        self.seconds.set(settings.pop('waitTime'))
        self.optionManger.destroyOptions()
        self.optionManger.setProfile(settings)

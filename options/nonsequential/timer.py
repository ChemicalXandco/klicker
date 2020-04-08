from tkinter import *
import time

import gui
import options.sequential
from options import Base
from options.numbers import Number


class Widget(Base):
    def __init__(self, *args):
        super().__init__(*args)

        self.frameOne = Frame(self.parent)
        self.frameOne.grid(row=0, column=self.spacing, sticky=W)

        self.labelOne = Label(self.frameOne, text='Every')
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
        self.interval = self.seconds.parse()
        self.addTime = 0

    def stop(self):
        return

    def update(self):
        if time.time() >= self.timer + self.addTime:
            self.optionManger.runOptions()
            self.addTime += self.interval

    def returnSettings(self):
        settings = self.optionManger.getProfile()
        settings['interval'] = self.seconds.get()
        return settings

    def addSettings(self, settings):
        self.seconds.set(settings.pop('interval'))
        self.optionManger.destroyOptions()
        self.optionManger.setProfile(settings)

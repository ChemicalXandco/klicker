from tkinter import *
import time

import gui
import options.sequential

class Widget:
    def __init__(self, parent, spacing):
        self.parent = parent

        self.frameOne = Frame(parent)
        self.frameOne.grid(row=0, column=spacing)

        self.labelOne = Label(self.frameOne, text='After')
        self.labelOne.grid(row=0, column=0, sticky=E)

        self.seconds = Entry(self.frameOne, width=5)
        self.seconds.grid(row=0, column=1)

        self.labelTwo = Label(self.frameOne, text='seconds')
        self.labelTwo.grid(row=0, column=2, sticky=W)

        self.options = LabelFrame(parent, text='do')
        self.options.grid(row=1, column=spacing, sticky=E)

        self.optionManger = gui.OptionManager(self.options, options.sequential.optList, True, 50)

    def start(self):
        self.timer = time.time()
        self.waitTime = float(self.seconds.get())
        self.hasRan = False

    def stop(self):
        return

    def update(self):
        timed = time.time()-self.timer
        if timed >= self.waitTime and not self.hasRan:
            self.hasRan = True
            self.optionManger.runOptions()

    def returnSettings(self):
        settings = self.optionManger.getProfile()
        settings['waitTime'] = self.seconds.get()
        return settings

    def addSettings(self, settings):
        self.seconds.delete(0,END)
        self.seconds.insert(0, settings.pop('waitTime'))
        self.optionManger.destroyOptions()
        self.optionManger.setProfile(settings)

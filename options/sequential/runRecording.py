from tkinter import *
from time import sleep

from options.sequential import SequentialBase
from options.recordings import replayRecording


class Widget(SequentialBase):
    def __init__(self, *args):
        super().__init__(*args)

        self.labelOne = Label(self.parent, text='Name of recording file:')
        self.labelOne.grid(row=0, column=self.spacing, sticky=E)

        self.recordingFilename = StringVar(self.parent)

        self.optionMenu = OptionMenu(self.parent, self.recordingFilename, '')
        self.optionMenu.grid(row=0, column=self.spacing+1)

        self.recordings.addUpdate(self.update)

    def update(self, optionList):
        menu = self.optionMenu["menu"]
        try:
            menu.delete(0, "end")
            for string in optionList:
                menu.add_command(label=string,
                                command=lambda value=string: self.recordingFilename.set(value))
        except AttributeError:
            return

    def run(self):
        replayRecording(self.recordingFilename.get(), self.logger)

    @property
    def settings(self):
        return { 'recordingFilename': self.recordingFilename.get() }

    @settings.setter
    def settings(self, settings):
        self.recordingFilename.set(settings['recordingFilename'])

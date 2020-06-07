from tkinter import *
from time import sleep
import pyautogui

from options import Base
from options.recordings import replayRecording


class Widget(Base):
    def __init__(self, *args):
        super().__init__(*args)

        self.labelOne = Label(self.parent, text='Name of recording file:')
        self.labelOne.grid(row=0, column=self.spacing, sticky=E)

        self.recordingFilename = Entry(self.parent, width=20)
        self.recordingFilename.grid(row=0, column=self.spacing+1)

    def run(self):
        replayRecording(self.recordingFilename.get(), self.logger)

    def returnSettings(self):
        settings = {}
        settings['recordingFilename'] = self.recordingFilename.get()
        return settings

    def addSettings(self, settings):
        self.recordingFilename.delete(0,END)
        self.recordingFilename.insert(0, settings['recordingFilename'])

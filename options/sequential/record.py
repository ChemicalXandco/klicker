from tkinter import *
from time import sleep
import uuid
import json

from options import Base
from options.utils import CheckList


class FakeWidget:
    def __init__(self, value=None):
        self.value = value

    def get(self):
        return self.value

    def destroy(self):
        pass


class Widget(Base):
    def __init__(self, *args):
        super().__init__(*args)

        label1 = Label(self.parent, text='Kill key')
        label1.grid(row=0, column=self.spacing, sticky=E)
        vcmd = (self.parent.register(self.limitChar), '%i')
        self.killKey = Entry(self.parent, validate='key', validatecommand=vcmd)
        self.killKey.grid(row=0, column=self.spacing+1, sticky=W)

        label2 = Label(self.parent, text='Name (optional)')
        label2.grid(row=1, column=self.spacing, sticky=E)
        self.newRecordingName = Entry(self.parent)
        self.newRecordingName.grid(row=1, column=self.spacing+1, sticky=W)

        self.types = CheckList(self.parent, ['Keyboard', 'Mouse Movements', 'Left Button', 'Right Button', 'Scroll', 'Store Timings'], default=0)
        self.types.grid(row=2, column=self.spacing, columnspan=2, sticky=W)

    def limitChar(self, i):
        if i == '1': # if the index is 1 it means the string will be 2 characters long
            return False
        return True

    def run(self):
        self.recordings.killKey = self.killKey
        if self.newRecordingName.get() != '':
            self.recordings.newRecordingName = self.newRecordingName
        else:
            self.recordings.newRecordingName = FakeWidget(str(uuid.uuid4())[:8])
        self.recordings.types = self.types
        self.recordings.childWindow = FakeWidget()
        self.recordings.record()

    def returnSettings(self):
        settings = {}
        settings['killKey'] = self.killKey.get()
        settings['name'] = self.newRecordingName.get()
        settings['types'] = json.dumps(self.types.get())
        return settings

    def addSettings(self, settings):
        self.killKey.delete(0,END)
        self.killKey.insert(0, settings['killKey'])
        self.newRecordingName.delete(0,END)
        self.newRecordingName.insert(0, settings['name'])
        self.types.update(json.loads(settings['types']), updateTo=1)
        self.types.update(['Keyboard', 'Mouse Movements', 'Left Button', 'Right Button', 'Scroll', 'Store Timings'])

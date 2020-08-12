from tkinter import *
from time import sleep
import uuid
import json

from options.sequential import SequentialBase
from options.utils import KeySelector, CheckList
import options.recordings


class FakeWidget:
    def __init__(self, value=None):
        self.value = value

    def get(self):
        return self.value

    def destroy(self):
        pass


class Widget(SequentialBase):
    def __init__(self, *args):
        super().__init__(*args)

        label1 = Label(self.parent, text='Kill key')
        label1.grid(row=0, column=self.spacing, sticky=E)
        self.killKey = KeySelector(self.parent, self.root)
        self.killKey.grid(row=0, column=self.spacing+1, sticky=W)

        label2 = Label(self.parent, text='Name (optional)')
        label2.grid(row=1, column=self.spacing, sticky=E)
        self.newRecordingName = Entry(self.parent)
        self.newRecordingName.grid(row=1, column=self.spacing+1, sticky=W)

        self.types = CheckList(self.parent, options.recordings.availableTypes, default=0)
        self.types.grid(row=2, column=self.spacing, columnspan=2, sticky=W)

    def run(self):
        self.recordings.killKey = self.killKey
        if self.newRecordingName.get() != '':
            self.recordings.newRecordingName = self.newRecordingName
        else:
            self.recordings.newRecordingName = FakeWidget(str(uuid.uuid4())[:8])
        self.recordings.types = self.types
        self.recordings.childWindow = FakeWidget()
        self.recordings.record()

    @property
    def settings(self):
        return {
            'killKey': self.killKey.get(),
            'name': self.newRecordingName.get(),
            'types': json.dumps(self.types.get()),
        }

    @settings.setter
    def settings(self, settings):
        self.killKey.set(settings['killKey'])
        self.newRecordingName.delete(0,END)
        self.newRecordingName.insert(0, settings['name'])
        self.types.update(json.loads(settings['types']), updateTo=1)
        self.types.update(options.recordings.availableTypes)

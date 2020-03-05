from tkinter import *
import time
import socket
from urllib.request import urlopen

socket.setdefaulttimeout(0.1)  # timeout in seconds

from options import Base

class Widget(Base):
    def __init__(self, *args):
        super().__init__(*args)

        self.labelOne = Label(self.parent, text='ping')
        self.labelOne.grid(row=0, column=self.spacing, sticky=E)

        self.url = Entry(self.parent, width=20)
        self.url.grid(row=0, column=self.spacing+1)

    def run(self):
        url = self.url.get()
        timer = time.time()
        try:
            response = urlopen(url)
            self.logger.debug('Time to ping {}: {} ms'.format(url, (time.time()-timer)*10))
        except Exception as e:
            self.logger.error(e)

    def returnSettings(self):
        settings = {}
        settings['url'] = self.url.get()
        return settings

    def addSettings(self, settings):
        self.url.delete(0,END)
        self.url.insert(0, settings['url'])

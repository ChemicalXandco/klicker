from tkinter import *
import time
import socket
from urllib.request import urlopen

socket.setdefaulttimeout(0.1)  # timeout in seconds


class Widget:
    def __init__(self, parent, spacing, logger):
        self.parent = parent

        self.labelOne = Label(parent, text='ping')
        self.labelOne.grid(row=0, column=spacing, sticky=E)

        self.url = Entry(parent, width=20)
        self.url.grid(row=0, column=spacing+1)

        self.logger = logger

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

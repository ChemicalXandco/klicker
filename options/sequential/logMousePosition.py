from tkinter import *
import pyautogui

class Widget:
    def __init__(self, parent, spacing, logger):
        self.parent = parent

        self.logger = logger
        
    def run(self):
        pos = pyautogui.position()
        self.logger.info('Mouse cursor at ({}, {})'.format(pos[0], pos[1]))

    def returnSettings(self):
        return {}

    def addSettings(self, settings):
        pass

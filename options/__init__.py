import pkgutil
import importlib
import os

def getOptions(path):
    optDict = {}
    for importer, package, ispkg in pkgutil.walk_packages(path):  
        optDict[package] = importlib.import_module('options.'+os.path.split(path[0])[1]+'.'+package)
    try:
        del optDict['abstract']
    except KeyError:
        pass
    return optDict, list(optDict.keys())


class OptionBase:
    '''
    Basic construct for all option widgets
    '''
    def __init__(self, parent, root, save, logger, numbers, recordings):
        self.parent = parent
        self.root = root
        self.save = save
        self.logger = logger
        self.numbers = numbers
        self.recordings = recordings

    @property
    def args(self):
        return [
            self.root,
            self.save,
            self.logger,
            self.numbers,
            self.recordings
        ]


class Base(OptionBase):
    '''
    Basic construct for option widgets with spacing
    '''
    def __init__(self, parent, spacing, *args):
        super().__init__(parent, *args)
        self.spacing = spacing

    @property
    def settings(self):
        return {}

    @settings.setter
    def settings(self, settings):
        return

import pkgutil
import importlib

from options import Base


class NonsequentialBase(Base):
    '''
    Basic construct for non-sequential option widgets
    '''
    def __init__(self, *args):
        super().__init__(*args)

    def start(self):
        return

    def stop(self):
        return

    def update(self):
        return


optDict = {}

for importer, package, ispkg in pkgutil.walk_packages(__path__):  
    optDict[package] = importlib.import_module('options.nonsequential.'+package)

del optDict['abstract']
    
optList = list(optDict.keys())


import pkgutil
import importlib

from options import Base


class SequentialBase(Base):
    '''
    Basic construct for sequential option widgets
    '''
    def __init__(self, *args):
        super().__init__(*args)

    def run(self):
        raise NotImplementedError()


optDict = {}

for importer, package, ispkg in pkgutil.walk_packages(__path__):  
    optDict[package] = importlib.import_module('options.sequential.'+package)

del optDict['abstract']
    
optList = list(optDict.keys())

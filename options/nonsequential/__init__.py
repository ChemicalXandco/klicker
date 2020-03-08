import pkgutil
import importlib

optDict = {}

for importer, package, ispkg in pkgutil.walk_packages(__path__):  
    optDict[package] = importlib.import_module('options.nonsequential.'+package)
    
optList = list(optDict.keys())


from options.sequential import (
scroll,
mouseDown,
mouseUp,
keyDown,
keyUp,
wait,
ping,
find,
moveMouseTo,
moveMouseRelative,
deactivate
)

optDict = {'scroll': scroll,
           'mouseDown': mouseDown,
           'mouseUp': mouseUp,
           'keyDown': keyDown,
           'keyUp': keyUp,
           'wait': wait,
           'ping': ping,
           'find': find,
           'moveMouseTo': moveMouseTo,
           'moveMouseRelative': moveMouseRelative,
           'deactivate': deactivate
           }

optList = list(optDict.keys())

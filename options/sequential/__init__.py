from options.sequential import (
scroll,
mouseDown,
mouseUp,
wait,
ping,
find,
moveMouseTo
)

optDict = {'scroll': scroll,
           'mouseDown': mouseDown,
           'mouseUp': mouseUp,
           'wait': wait,
           'ping': ping,
           'find': find,
           'moveMouseTo': moveMouseTo
           }

optList = list(optDict.keys())

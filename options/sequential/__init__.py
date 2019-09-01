from options.sequential import (
scroll,
mouseDown,
mouseUp,
wait,
ping,
find
)

optDict = {'scroll': scroll,
           'mouseDown': mouseDown,
           'mouseUp': mouseUp,
           'wait': wait,
           'ping': ping,
           'find': find
           }

optList = list(optDict.keys())

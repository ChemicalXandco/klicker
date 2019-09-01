from options.sequential import (
scroll,
mouseDown,
mouseUp,
wait,
ping
)

optDict = {'scroll': scroll,
           'mouseDown': mouseDown,
           'mouseUp': mouseUp,
           'wait': wait,
           'ping': ping
           }

optList = list(optDict.keys())

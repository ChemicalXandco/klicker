import sys, keyboard
from time import time, sleep
from tkinter import *

from gui import *
from options.utils import DeactivateRequest

root = Tk()
gui = GUI(root)
gui.clearLog()
keys = [i[0] for i in keyboard._winkeyboard.official_virtual_keys.values()]
activated = False
currentButton = None
warning = 'Cannot activate autoclick when this GUI is in focus'
focus = False
while True:
    try:
        if root.focus_get() != None:
            if not focus:
                gui.logger.warning(warning)
            focus = True
        else:
            focus = False
            if gui.hotkey.get() in keys:
                if keyboard.is_pressed(gui.hotkey.get()):
                    if activated:
                        raise DeactivateRequest('Hotkey pressed - deactivated')
                    else:
                        sleep(1)
                        activated = True
                        gui.status.config(text='Active', fg='#00ff00')
                        gui.optionManager.startOptions()
                        timer = time()
                        gui.uptime.config(fg='#00ff00')
        if activated:
            gui.optionManager.updateOptions()
            gui.uptime.config(text=str(round(time()-timer, 2)))
        root.update_idletasks()
        root.update()
        sleep(0.01)#minimise CPU usage
    except DeactivateRequest as e:
        gui.logger.info(e)
        gui.optionManager.stopOptions()
        gui.status.config(text='Inactive', fg='#ff0000')
        activated = False
        gui.uptime.config(fg='#ff0000')
        sleep(1)
    except Exception as e:
        try:
            gui.logger.error(e)
            root.update_idletasks()
            root.update()
        except TclError:
            sys.exit()



import sys, keyboard
import time
from tkinter import *

from gui import *
from options.utils import DeactivateRequest

root = Tk()
gui = GUI(root)
gui.clearLog()
try:
    keyboard._os_keyboard.init()
    keys = list(dict.fromkeys([i[0] for i in keyboard._os_keyboard.to_name.values()]))
except Exception as e:
    keys = ['x']
    gui.logger.warning('Keys failed to load, only x can be used as an activation hotkey: '+str(e))
activated = False
released = False
lastProfileSwap = time.time()
timer = time.time()

while True:
    try:
        if gui.hotkey.get() in keys:
            if keyboard.is_pressed(gui.hotkey.get()):
                if activated and released:
                    raise DeactivateRequest('Hotkey pressed - deactivated')
                else:
                    if root.focus_get() != None:
                        gui.logger.warning('Cannot activate while this window is in focus')
                        timer = time.time()
                    elif not activated:
                        activated = True
                        released = False
                        gui.status.config(text='Active', fg='#00ff00')
                        gui.uptime.config(fg='#00ff00')
                        if gui.overlay.get() == 1:
                            gui.enableOverlay()
                        gui.logger.system('Hotkey pressed - activated')
                        timer = time.time()
                        gui.optionManager.startOptions()
            elif not released:
                released = True
        if gui.profileHotkey.get() in keys:
            if keyboard.is_pressed(gui.profileHotkey.get()):
                if time.time()-lastProfileSwap > 0.1:
                    lastProfileSwap = time.time()
                    gui.nextProfile()
        if activated:
            gui.optionManager.updateOptions()
            gui.uptime.config(text=str(round(time.time()-timer, 2)))
        else:
            gui.checkToDisableOverlay()
        root.update_idletasks()
        root.update()
        time.sleep(0.01) # minimise CPU usage
    except DeactivateRequest as e:
        gui.logger.system(e)
        gui.timeSinceOverlayOpened = time.time()
        gui.optionManager.stopOptions()
        gui.status.config(text='Inactive', fg='#ff0000')
        activated = False
        gui.uptime.config(fg='#ff0000')
        time.sleep(1)
    except Exception as e:
        try:
            gui.logger.error(e)
            root.update_idletasks()
            root.update()
        except TclError:
            sys.exit()



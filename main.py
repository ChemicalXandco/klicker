import sys
import time
from tkinter import *

from pynput import keyboard

from gui import *
from options.utils import DeactivateRequest

root = Tk()
gui = GUI(root)
gui.clearLog()

activated = False
timer = time.time()
with keyboard.Events() as events:
    while True:
        try:
            event = events.get(0.01)
            if isinstance(event, keyboard.Events.Press):
                if event.key == gui.hotkey.key:
                    if activated:
                        raise DeactivateRequest('Hotkey pressed - deactivated')
                    elif root.focus_get() != None:
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
                        # start options
                        gui.numbers.registerSettings()
                        gui.optionManager.registerSettings()
                        gui.optionManager.startOptions()
                if event.key == gui.profileHotkey.key:
                    if activated:
                        gui.logger.warning('Could not switch profile because the system is activated.')
                    elif root.focus_get() != None:
                        gui.logger.warning('Could not switch profile because this window is in focus.')
                    else:
                        gui.nextProfile()
            if activated:
                gui.uptime.config(text=str(round(time.time()-timer, 2)))
                gui.updateTextHandlers()
            else:
                gui.checkToDisableOverlay()
            root.update_idletasks()
            root.update()
        except TclError:
            sys.exit()
        except Exception as e:
            if isinstance(e, DeactivateRequest):
                gui.logger.system(e)
            else:
                gui.logger.error(e)
            if activated:
                gui.timeSinceOverlayOpened = time.time()
                gui.optionManager.stopOptions()
                gui.status.config(text='Inactive', fg='#ff0000')
                activated = False
                gui.uptime.config(fg='#ff0000')

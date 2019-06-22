import sys, pyautogui, keyboard
from time import sleep
from tkinter import *

import options

class GUI:
    def __init__(self, master):
        self.master = master
        master.title('Simple Clicker')
        master.iconbitmap('icon.ico')
        master.geometry("200x200")

        self.hotkeyLabel = Label(master, text='Hotkey')
        vcmd = (master.register(self.limitChar), '%i')
        self.hotkey = Entry(master, validate='key', validatecommand=vcmd, width=2)
        self.hotkeyLabel.grid(row=0, column=0)
        self.hotkey.grid(row=0, column=1)

        self.addOption = StringVar(master)
        self.addOption.set('➕')
        self.addOptions = OptionMenu(master, self.addOption, *options.optList, command=self.handleAddOption)
        self.addOptions.grid(row=1, column=1)
        
        self.options = LabelFrame(master, text='Options')
        self.options.grid(row=2, column=0, columnspan=2)

        self.optionWidgets = []

        self.refreshButton = Button(master, text='Refresh Options From File', command=self.readSetting)
        self.refreshButton.grid(row=3, column=0, columnspan=2)

        self.saveButton = Button(master, text='Save Options To File', command=self.writeSetting)
        self.saveButton.grid(row=4, column=0, columnspan=2)

        self.error = Label(master, text='', fg='#ff0000', wraplengt=master.winfo_width())
        self.error.grid(row=5, column=0, columnspan=2)

        self.readSetting()

    def limitChar(self, i):
        if i == '1': #if the index is 1 it means the string will be 2 characters long
            return False
        else:
            return True

    def handleAddOption(self, *args):
        if len(self.optionWidgets) < 10:
            self.optionWidgets.append(OptionWrapper(self.options, self.addOption.get()))
        else:
            self.error.config(text='Too many options')
        self.addOption.set('➕')

    def readSetting(self):
        f = open('config.ini', 'r')
        self.hotkey.delete(0, END)
        self.hotkey.insert(0, f.readline().strip())
        f.close

    def writeSetting(self):
        f = open('config.ini', 'w')
        f.write(self.hotkey.get()+'\n')
        f.close()

class OptionWrapper:
    def __init__(self, master, option):
        self.frame = LabelFrame(master, text=option)

        self.deleteButton = Button(self.frame, text='❌', command=self.findIdAndDestroy)
        self.deleteButton.grid(row=0, column=0)

        options.optDict.get(option).Widget(self.frame, 1)
        
        self.frame.pack()

    def findIdAndDestroy(self):
        for i in gui.optionWidgets:
            if id(i) == id(self):
                gui.optionWidgets.remove(i)
        self.frame.destroy()

root = Tk()
gui = GUI(root)
keys = [i[0] for i in keyboard._winkeyboard.official_virtual_keys.values()]
click = False
currentButton = None
warning = 'Cannot activate autoclick when this GUI is in focus'
focus = False
while True:
    try:
        if root.focus_get() != None:
            if not focus:
                gui.error.config(text=warning)
            focus = True
        else:
            if gui.error.cget('text') == warning:
                gui.error.config(text='')
                focus = False
            if gui.hotkey.get() in keys:
                if keyboard.is_pressed(gui.hotkey.get()):
                    if click:
                        pyautogui.mouseUp(button=currentButton)
                        click = False
                    else:
                        currentButton = gui.choice.get()
                        pyautogui.mouseDown(button=currentButton)
                        click = True
                    sleep(1)
        root.update_idletasks()
        root.update()
        sleep(0.01)#minimise CPU usage
    except Exception as e:
        try:
            gui.error.config(text=e)
        except TclError:
            sys.exit()
    
    

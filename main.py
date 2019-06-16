import sys, pyautogui, keyboard
from time import sleep
from tkinter import *

class GUI:
    def __init__(self, master):
        self.master = master
        master.title('Simple Clicker')
        master.iconbitmap('icon.ico')
        master.geometry("200x200")

        self.options = LabelFrame(master, text='Options')
        self.options.pack()

        self.hotkeyLabel = Label(self.options, text='Hotkey')
        vcmd = (master.register(self.limitChar), '%i')
        self.hotkey = Entry(self.options, validate='key', validatecommand=vcmd, width=2)
        self.hotkeyLabel.grid(row=0, column=0)
        self.hotkey.grid(row=0, column=1)

        self.choices = ['left', 'right']
        self.choice = StringVar(master)
        self.choice.set(self.choices[0])
        self.mouseClickLabel = Label(self.options, text='Mouse Button')
        self.mouseClick = OptionMenu(self.options, self.choice, *self.choices)
        self.mouseClickLabel.grid(row=1, column=0)
        self.mouseClick.grid(row=1, column=1)

        self.refreshButton = Button(self.options, text='Refresh Options From File', command=self.readSetting)
        self.refreshButton.grid(row=2, column=1)

        self.saveButton = Button(self.options, text='Save Options To File', command=self.writeSetting)
        self.saveButton.grid(row=3, column=1)

        self.error = Label(master, text='', fg='#ff0000', wraplengt=master.winfo_width())
        self.error.pack()

        self.readSetting()

    def limitChar(self, i):
        if i == '1': #if the index is 1 it means the string will be 2 characters long
            return False
        else:
            return True

    def readSetting(self):
        f = open('config.ini', 'r')
        self.hotkey.delete(0, END)
        self.hotkey.insert(0, f.readline().strip())
        self.choice.set(f.readline().strip())
        f.close

    def writeSetting(self):
        f = open('config.ini', 'w')
        f.write(self.hotkey.get()+'\n')
        f.write(self.choice.get())
        f.close()

root = Tk()
gui = GUI(root)
keys = [i[0] for i in keyboard._winkeyboard.official_virtual_keys.values()]
click = False
currentButton = None
warning = 'Cannot activate autoclick when this GUI is in focus'
while True:
    try:
        if root.focus_get() != None:
            gui.error.config(text=warning)
        else:
            if gui.error.cget('text') == warning:
                gui.error.config(text='')
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
    
    

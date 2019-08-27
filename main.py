import sys, keyboard
from time import time, sleep
from tkinter import *

import options
import profile_manager as profileManager

class GUI:
    def __init__(self, master):
        self.master = master
        master.title('Simple Clicker')
        master.iconbitmap('icon.ico')

        self.status = Label(master, text='Inactive', fg='#ff0000')
        self.status.grid(row=0, column=0)

        self.uptime = Label(master, text='0', fg='#ff0000', width=20)
        self.uptime.grid(row=0, column=1)

        self.config = LabelFrame(master, text='Configuration')
        self.config.grid(row=1, column=0, columnspan=2, sticky=W, padx=5, pady=5)

        self.hotkeyFrame = Frame(self.config)
        self.hotkeyFrame.grid(row=0, column=0, sticky=W)

        self.hotkeyLabel = Label(self.hotkeyFrame, text='Hotkey')
        vcmd = (master.register(self.limitChar), '%i')
        self.hotkey = Entry(self.hotkeyFrame, validate='key', validatecommand=vcmd, width=2)
        self.hotkeyLabel.grid(row=0, column=0, sticky=E)
        self.hotkey.grid(row=0, column=1, sticky=W)

        self.profiles = LabelFrame(self.config, text='Profile')
        self.profiles.grid(row=2, column=0, columnspan=2, sticky=W, padx=5, pady=5)

        self.profileLabel = Label(self.profiles, text='Set Profile')
        self.profileLabel.grid(row=1, column=0)

        self.addProfile = Button(self.profiles, text='➕', command=self.handleAddProfile)
        self.addProfile.grid(row=1, column=2)

        self.profile = StringVar(master)
        self.setProfile = OptionMenu(self.profiles, self.profile, *self.profileList(), command=self.handleSetProfile)
        self.setProfile.grid(row=1, column=1)

        self.delProfile = Button(self.profiles, text='❌', command=self.handleConfirmDelProfile)
        self.delProfile.grid(row=1, column=3)

        self.refreshButton = Button(self.config, text='Refresh Configuration', command=self.readSetting)
        self.refreshButton.grid(row=3, column=0)

        self.saveButton = Button(self.config, text='Save Configuration', command=self.writeSetting)
        self.saveButton.grid(row=3, column=1)

        self.addOptionFrame = Frame(master)
        self.addOptionFrame.grid(row=2, column=0, sticky=W)

        self.addOptionLabel = Label(self.addOptionFrame, text='Add Option')
        self.addOptionLabel.grid(row=0, column=0, sticky=E)

        self.addOption = StringVar(master)
        self.addOption.set('➕')
        self.addOptions = OptionMenu(self.addOptionFrame, self.addOption, *options.optList, command=self.handleAddOption)
        self.addOptions.grid(row=0, column=1, sticky=W)
        
        self.options = LabelFrame(master, text='Options')
        self.options.grid(row=3, column=0, columnspan=2, sticky=W, padx=5, pady=5)

        self.optionWidgets = []

        self.error = Label(master, text='', fg='#ff0000', wraplengt=master.winfo_width())
        self.error.grid(row=6, column=0, columnspan=2)

        self.readSetting()

    def limitChar(self, i):
        if i == '1': #if the index is 1 it means the string will be 2 characters long
            return False
        else:
            return True

    def profileList(self):
        profiles = list(profileManager.read().keys())
        if profiles == []:
            profiles = [None]
        return profiles

    def handleAddProfile(self):
        self.childWindow = Toplevel(self.master)
        self.childWindow.title('Name Profile')
        self.childWindow.iconbitmap('icon.ico')
        self.childWindow.geometry('250x50')
        self.newProfileName = Entry(self.childWindow)
        self.newProfileName.pack(fill=X, expand=YES)
        createButton = Button(self.childWindow, text="Create", command=self.handleCreateProfile)
        createButton.pack(fill=X, expand=YES)

    def handleCreateProfile(self):
        profile = {}
        occurrences = {}
        for o in self.optionWidgets:
            if not o.name in occurrences:
                occurrences[o.name] = 0
            else:
                occurrences[o.name] += 1
            optionName = '{}-{}'.format(o.name, occurrences[o.name])
            profile[optionName] = o.widget.returnSettings()
        profileManager.write(self.newProfileName.get(), profile)
        self.refreshProfiles()
        self.profile.set(self.newProfileName.get())
        self.childWindow.destroy()
        self.handleSetProfile()

    def handleSetProfile(self, *args):
        while self.optionWidgets != []:
            for o in self.optionWidgets:
                o.findIdAndDestroy()
        
        profile = self.profile.get()
        profiles = profileManager.read()
        for option, attributes in profiles[profile].items():
            self.optionWidgets.append(OptionWrapper(self.options, option.split('-')[0]))
            self.optionWidgets[-1].widget.addSettings(attributes)

    def menuCommand(self, value):
        self.profile.set(value)
        self.handleSetProfile()

    def refreshProfiles(self):
        profiles = self.profileList()
        
        menu = self.setProfile['menu']
        menu.delete(0, END)
        for string in profiles:
            menu.add_command(label=string, 
                             command=lambda value=string: self.menuCommand(value))

    def handleConfirmDelProfile(self):
        self.childWindow = Toplevel(self.master)
        self.childWindow.title('Confirm Delete Profile')
        self.childWindow.iconbitmap('icon.ico')
        self.childWindow.geometry('300x50')
        label = Label(self.childWindow, text='Delete Profile "{}"?'.format(self.profile.get()))
        label.pack(fill=X, expand=YES)
        createButton = Button(self.childWindow, text="Delete", command=self.handleDelProfile)
        createButton.pack(fill=X, expand=YES)

    def handleDelProfile(self):
        self.childWindow.destroy()
        profileManager.remove(self.profile.get())
        self.refreshProfiles()
        self.profile.set('')

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
        self.profile.set(f.readline().strip())
        if self.profile.get() in self.profileList():
            self.handleSetProfile()
        f.close
        self.refreshProfiles()

    def writeSetting(self):
        f = open('config.ini', 'w')
        f.write(self.hotkey.get()+'\n')
        f.write(self.profile.get())
        f.close()

class OptionWrapper:
    def __init__(self, master, option):
        self.frame = LabelFrame(master, text=option)

        self.deleteButton = Button(self.frame, text='❌', command=self.findIdAndDestroy)
        self.deleteButton.grid(row=0, column=0)

        self.name = option
        self.widget = options.optDict.get(option).Widget(self.frame, 1)
        
        self.frame.pack(anchor=W, padx=5, pady=5)

    def findIdAndDestroy(self):
        for i in gui.optionWidgets:
            if id(i) == id(self):
                gui.optionWidgets.remove(i)
        self.frame.destroy()

if __name__ == '__main__':
    root = Tk()
    gui = GUI(root)
    keys = [i[0] for i in keyboard._winkeyboard.official_virtual_keys.values()]
    activated = False
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
                focus = False
                if gui.error.cget('text') == warning:
                    gui.error.config(text='') 
                if gui.hotkey.get() in keys:
                    if keyboard.is_pressed(gui.hotkey.get()):
                        if activated:
                            for o in gui.optionWidgets:
                                o.widget.stop()
                            gui.status.config(text='Inactive', fg='#ff0000')
                            activated = False
                            gui.uptime.config(fg='#ff0000')
                            sleep(1)
                        else:
                            sleep(1)
                            activated = True
                            gui.status.config(text='Active', fg='#00ff00')
                            for o in gui.optionWidgets:
                                o.widget.start()
                            timer = time()
                            gui.uptime.config(fg='#00ff00')
            if activated:
                for o in gui.optionWidgets:
                    o.widget.update()
                gui.uptime.config(text=str(round(time()-timer, 2)))
            root.update_idletasks()
            root.update()
            sleep(0.01)#minimise CPU usage
        except Exception as e:
            try:
                gui.error.config(text=e)
                root.update_idletasks()
                root.update()
            except TclError:
                sys.exit()
    
    

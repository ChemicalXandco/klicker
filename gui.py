from tkinter import *

import options.sequential, options.nonsequential
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

        self.profile = StringVar(master)
        self.setProfile = OptionMenu(self.profiles, self.profile, *self.profileList(), command=self.handleSetProfile)
        self.setProfile.grid(row=1, column=1)

        self.saveProfile = Button(self.profiles, text='Save', command=self.handleSaveProfile)
        self.saveProfile.grid(row=1, column=2)

        self.addProfile = Button(self.profiles, text='➕', command=self.handleAddProfile)
        self.addProfile.grid(row=1, column=3)

        self.delProfile = Button(self.profiles, text='❌', command=self.handleConfirmDelProfile)
        self.delProfile.grid(row=1, column=4)

        self.refreshButton = Button(self.config, text='Refresh Configuration', command=self.readSetting)
        self.refreshButton.grid(row=3, column=0)

        self.saveButton = Button(self.config, text='Save Configuration', command=self.writeSetting)
        self.saveButton.grid(row=3, column=1)

        self.addOptionFrame = Frame(master)
        self.addOptionFrame.grid(row=2, column=0, sticky=W)
        
        self.options = LabelFrame(master, text='Options')
        self.options.grid(row=3, column=0, columnspan=2, sticky=W, padx=5, pady=5)

        self.optionManager = OptionManager(self.options, options.nonsequential.optList, 10) 

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

    def handleSaveProfile(self):
        self.newProfileName = Entry(self.master)
        self.newProfileName.delete(0, END)
        self.newProfileName.insert(0, self.profile.get())
        self.handleCreateProfile()

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
        profile = self.optionManager.getProfile()
        profileManager.write(self.newProfileName.get(), profile)
        self.refreshProfiles()
        self.profile.set(self.newProfileName.get())
        try:
            self.childWindow.destroy()
        except AttributeError:
            pass
        self.handleSetProfile()

    def handleSetProfile(self, *args): 
        self.optionManager.destroyOptions()
        self.optionManager.setProfile(profileManager.read()[self.profile.get()])

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
    def __init__(self, master, sequential, option, widgets):
        self.widgets = widgets
        
        self.frame = LabelFrame(master, text=option)

        self.deleteButton = Button(self.frame, text='❌', command=self.findIdAndDestroy)
        self.deleteButton.grid(row=0, column=0)

        self.name = option
        
        if sequential:
            optionObject = options.sequential.optDict.get(option)
        else:
            optionObject = options.nonsequential.optDict.get(option)
        self.widget = optionObject.Widget(self.frame, 1)
        
        self.frame.pack(anchor=W, padx=5, pady=5)

    def findIdAndDestroy(self):
        for i in self.widgets:
            if id(i) == id(self):
                self.widgets.remove(i)
        self.frame.destroy()


class OptionManager:
    def __init__(self, parent, availableOptions, maxOptions, sequential=False):
        self.parent = parent
        self.max = maxOptions
        self.sequential = sequential

        self.addOptionFrame = Frame(parent)
        self.addOptionFrame.pack()
        
        self.addOptionLabel = Label(self.addOptionFrame, text='Add Option')
        self.addOptionLabel.grid(row=0, column=0, sticky=E)

        self.selectedOption = StringVar(parent)
        self.selectedOption.set('➕')
        self.addOptions = OptionMenu(self.addOptionFrame, self.selectedOption, *availableOptions, command=self.handleAddOption)
        self.addOptions.grid(row=0, column=1, sticky=W)

        self.wrappers = []

    def handleAddOption(self, *args):
        if len(self.wrappers) < self.max:
            self.addOption(self.selectedOption.get())
        self.selectedOption.set('➕')

    def addOption(self, option):
        self.wrappers.append(OptionWrapper(self.parent, self.sequential, option, self.wrappers))

    def startOptions(self):
        for o in self.wrappers:
            o.widget.start() 

    def stopOptions(self):
        for o in self.wrappers:
            o.widget.stop()

    def updateOptions(self):
        for o in self.wrappers:
            o.widget.update()

    def runOptions(self):
        for o in self.wrappers:
            o.widget.run()

    def destroyOptions(self):
        while self.wrappers != []:
            for o in self.wrappers:
                o.findIdAndDestroy()

    def getProfile(self):
        profile = {}
        occurrences = {}
        
        for o in self.wrappers:
            if not o.name in occurrences:
                occurrences[o.name] = 0
            else:
                occurrences[o.name] += 1
            optionName = '{}-{}'.format(o.name, occurrences[o.name])
            profile[optionName] = o.widget.returnSettings()
            
        return profile

    def setProfile(self, profile):
        for option, attributes in profile.items():
            self.addOption(option.split('-')[0])
            self.wrappers[-1].widget.addSettings(attributes)

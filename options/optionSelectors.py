from tkinter import *

import options
from options import OptionBase


class OptionWrapper(OptionBase):
    def __init__(self, parent, optionType, option, *args, wrappersList=None, destroyCommand=None):
        super().__init__(parent, *args)

        self.widgets = wrappersList
        
        self.frame = LabelFrame(parent, text=option)

        if not destroyCommand:
            destroyCommand = self.findId
        self.deleteButton = Button(self.frame, text='❌', command=destroyCommand)
        self.deleteButton.grid(row=0, column=0)

        self.name = option
        
        if optionType.movable:
            self.upDownFrame = Frame(self.frame)
            self.upDownFrame.grid(row=0, column=1)

            fontSize = 9
            self.upButton = Button(self.upDownFrame, text='↑', font=font.Font(size=fontSize), command=lambda: self.swap(-1))
            self.upButton.grid(row=0, column=0)
            self.downButton = Button(self.upDownFrame, text='↓', font=font.Font(size=fontSize), command=lambda: self.swap(1))
            self.downButton.grid(row=0, column=1)
            columnSpace = 3
        else:
            columnSpace = 1
        optionObject = optionType.optDict.get(option)
        self.widget = optionObject.Widget(self.frame, columnSpace, *args)
        
        self.frame.pack(anchor=W, padx=5, pady=0)

    def findId(self, destroy=True):
        idx = 0
        for i in self.widgets:
            if id(i) == id(self):
                if destroy:
                    self.widgets.remove(i)
                else:
                    return idx
            idx += 1
        self.frame.destroy()

    def swap(self, to):
        index = self.findId(False)
        toIndex = index + to
        try:
            if toIndex < 0:
                raise IndexError()
            self.widgets[toIndex], self.widgets[index] = self.widgets[index], self.widgets[toIndex]
            self.save()
        except IndexError:
            self.logger.warning('Could not move option.')


class OptionList(OptionBase):
    def __init__(self, parent, optionType, *args):
        super().__init__(parent, *args)

        self.optionType = optionType

        self.addOptionFrame = Frame(parent)
        self.addOptionFrame.pack()
        
        self.addOptionLabel = Label(self.addOptionFrame, text='Add Option')
        self.addOptionLabel.grid(row=0, column=0, sticky=E)

        self.selectedOption = StringVar(parent)
        self.selectedOption.set('➕')
        self.addOptions = OptionMenu(self.addOptionFrame, self.selectedOption, *optionType.optList, command=self.handleAddOption)
        self.addOptions.grid(row=0, column=1, sticky=W)

        self.wrappers = []

    def handleAddOption(self, *args):
        self.addOption(self.selectedOption.get())
        
        self.selectedOption.set('➕')

    def addOption(self, option):
        self.wrappers.append(OptionWrapper(self.parent, self.optionType, option, *self.args, wrappersList=self.wrappers))

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
                o.findId()

    def getProfile(self):
        profile = { 'options': [] }
        
        for o in self.wrappers:
            store = {}
            store['name'] = o.name
            store['settings'] = o.widget.returnSettings()
            profile['options'].append(store)

        return profile

    def setProfile(self, profile):
        for store in profile['options']:
            self.addOption(store['name'])
            self.wrappers[-1].widget.addSettings(store['settings'])


class SingleOption(OptionBase):
    def __init__(self, parent, optionType, *args, row=0, column=0):
        super().__init__(parent, *args)

        self.optionType = optionType

        self.frame = Frame(parent)
        self.frame.grid(row=row, column=column)

        self.showList()

    def showList(self):
        try: 
            self.option.frame.destroy()
        except AttributeError:
            pass
        self.selectedOption = StringVar(self.parent)
        self.selectedOption.set('Click to select')
        self.addOptions = OptionMenu(self.frame, self.selectedOption, *self.optionType.optList, command=self.showOption)
        self.addOptions.pack()

    def showOption(self, option):
        self.addOptions.destroy()
        self.option = OptionWrapper(self.frame, self.optionType, option, *self.args, destroyCommand=self.showList)

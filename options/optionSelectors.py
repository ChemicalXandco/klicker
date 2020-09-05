from tkinter import *
import threading

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


class Thread(threading.Thread):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.exception = None

    def run(self):
        try:
            super().run()
        except Exception as e:
            self.exception = e

    def join(self):
        super().join()
        return self.exception


class LoopThread(Thread):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._stopped = False

    def stop(self):
        self._stopped = True

    def run(self):
        while True:
            try:
                if self._target:
                    self._target(*self._args, **self._kwargs)
            except Exception as e:
                self.exception = e
            if self._stopped:
                break


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

    def registerSettings(self):
        for o in self.wrappers:
            o.widget.registerSettings()

    def resetStates(self):
        for o in self.wrappers:
            o.widget.resetState()

    def runParallel(self, threads, join=True):
        for thread in threads:
            thread.start()
        if join:
            self.joinThreads(threads, stop=False)

    def joinThreads(self, threads, stop=True):
        exceptions = []
        for thread in threads:
            if stop:
                thread.stop()
            exceptions.append(thread.join())
        for exception in exceptions:
            if exception:
                raise exception

    def startOptions(self):
        self.resetStates()
        self.runParallel([ Thread(target=o.widget.start) for o in self.wrappers ])

        self.threads = [ LoopThread(target=o.widget.update) for o in self.wrappers ]
        self.runParallel(self.threads, join=False)

    def stopOptions(self):
        try:
            if hasattr(self, 'threads'):
                self.joinThreads(self.threads)
                del self.threads
        finally:
            self.runParallel([ Thread(target=o.widget.stop) for o in self.wrappers ])

    def runOptions(self):
        for o in self.wrappers:
            o.widget.run()

    def destroyOptions(self):
        while self.wrappers != []:
            for o in self.wrappers:
                o.findId()

    @property
    def settings(self):
        return [ {
            'name': o.name,
            'settings': o.widget.settings,
        } for o in self.wrappers ]

    @settings.setter
    def settings(self, settings):
        for store in settings:
            try:
                self.addOption(store['name'])
                self.wrappers[-1].widget.settings = store['settings']
            except KeyError as e:
                if 'name' in store:
                    name = store['name']
                else:
                    name = '<unknown>'
                self.logger.error('Key error at {}: {}'.format(name, e))


class SingleOption(OptionBase):
    def __init__(self, parent, optionType, *args, row=0, column=0):
        super().__init__(parent, *args)

        self.optionType = optionType

        self.frame = Frame(parent)
        self.frame.grid(row=row, column=column)

        self._showList()

    def _showList(self):
        try:
            self.option.frame.destroy()
        except AttributeError:
            pass
        self.selectedOption = StringVar(self.parent)
        self.selectedOption.set('Click to select')
        self.addOptions = OptionMenu(self.frame, self.selectedOption, *self.optionType.optList, command=self._showOption)
        self.addOptions.pack()
        self.optionAvailable = False

    def _showOption(self, option):
        self.addOptions.destroy()
        self.option = OptionWrapper(self.frame, self.optionType, option, *self.args, destroyCommand=self._showList)
        self.optionAvailable = True

    def registerSettings(self):
        self.option.widget.registerSettings()

    def resetState(self):
        self.option.widget.resetState()

    def evaluateOption(self):
        return self.option.widget.evaluate()

    def getOption(self):
        return self.option.widget.get()

    @property
    def settings(self):
        if not self.optionAvailable:
            self.logger.warning("Could not save '{}'".format(self.optionType))
            return {}
        return {
            'name': self.option.name,
            'settings': self.option.widget.settings,
        }

    @settings.setter
    def settings(self, settings):
        try:
            self._showOption(settings['name'])
            self.option.widget.settings = settings['settings']
        except KeyError as e:
            if 'name' in settings:
                name = settings['name']
            else:
                name = '<unknown>'
            self.logger.error('Key error at {}: {}'.format(name, e))

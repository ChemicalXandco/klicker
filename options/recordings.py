import pynput
import os
from tkinter import *

import gui


class RecordingsFile:
    def __init__(self):
        self.killKey = None
        self.path = None

    def listItems(self):
        return os.listdir('recordings')

    def write(self, string):
        with open(self.path, 'a') as f:
            f.write(string + '\n')

    def remove(self, file):
        path = 'recordings/' + file
        if os.path.isfile(path):
            os.remove(path)

    def on_press(self, key):
        if key == self.killKey:
            return False
        self.write("KP {0}".format(key))

    def on_release(self, key):
        self.write("KR {0}".format(key))

    def on_move(self, x, y):
        self.write("MM ({0}, {1})".format(x, y))

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.write('MP ({0}, {1}) {2}'.format(x, y, button))
        else:
            self.write('MR ({0}, {1}) {2}'.format(x, y, button))

    def on_scroll(self, x, y, dx, dy):
        self.write('MS ({0}, {1})({2}, {3})'.format(x, y, dx, dy))

class Recordings(LabelFrame):
    def __init__(self, parent, text, logger, root):
        super().__init__(parent, text=text)
        self.master = parent
        self.logger = logger
        self.root = root

        self.widgets = []

        self.addButton = Button(self, text='➕', command=self.add)
        self.addButton.grid(row=0, column=0)

        self.recordingsGrid = Frame(self)
        self.recordingsGrid.grid(row=1, column=0)

        self.recordingsFile = RecordingsFile()

        self.update()

    def limitChar(self, i):
        if i == '1': # if the index is 1 it means the string will be 2 characters long
            return False
        return True

    def add(self):
        self.childWindow = Toplevel(self.master)
        self.childWindow.title('Name Recording')
        gui.GUI.setWindowIcon(self.childWindow)
        self.childWindow.geometry('250x110')
        label1 = Label(self.childWindow, text='Name')
        label1.pack()
        self.newRecordingName = Entry(self.childWindow)
        self.newRecordingName.pack(fill=X, expand=YES)
        label2 = Label(self.childWindow, text='Kill key')
        label2.pack()
        vcmd = (self.register(self.limitChar), '%i')
        self.killKey = Entry(self.childWindow, validate='key', validatecommand=vcmd)
        self.killKey.pack(fill=X, expand=YES)
        createButton = Button(self.childWindow, text="Record", command=self.record)
        createButton.pack(fill=X, expand=YES)

    def record(self):
        if self.killKey.get() == '':
            self.logger.error('Must set kill key for recording.')
        elif self.newRecordingName.get() == '':
            self.logger.error('Must set name for recording.')
        else:
            self.recordingsFile.killKey = pynput.keyboard.KeyCode(char=self.killKey.get())
            if not os.path.exists('recordings'):
                os.makedirs('recordings')
            self.recordingsFile.path = 'recordings/{}.txt'.format(self.newRecordingName.get())
            self.childWindow.destroy()
            self.logger.system('Recording Started.')
            self.root.update() # root needs to be updated for log message to show

            keyboardListener = pynput.keyboard.Listener(on_press=self.recordingsFile.on_press, 
                                                on_release=self.recordingsFile.on_release)
            mouseListener = pynput.mouse.Listener(on_move=self.recordingsFile.on_move, 
                                        on_click=self.recordingsFile.on_click, 
                                        on_scroll=self.recordingsFile.on_scroll)

            keyboardListener.start()
            mouseListener.start()
            keyboardListener.join()
            mouseListener.stop()
            mouseListener.join()
            self.logger.system('Recording Stopped.')
            self.update()

    def update(self):
        for b,l in self.widgets:
            b.destroy()
            l.destroy()
        self.widgets = []
        
        row = 0
        for i in self.recordingsFile.listItems():
            self.widgets.append(
                (   
                    Button(self.recordingsGrid, text='❌', command=lambda: self.remove(i)),
                    Label(self.recordingsGrid, text=i), 
                )
            )
            self.widgets[row][0].grid(row=row, column=0)
            self.widgets[row][1].grid(row=row, column=1)

            row += 1

    def remove(self, item):
        self.recordingsFile.remove(item)
        self.update()

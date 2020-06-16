import pynput
import os
import time
from datetime import datetime
from tkinter import *

import gui
from options.utils import KeySelector, CheckList


class RecordingsFile:
    def __init__(self):
        self.killKey = None
        self.path = None
        self.allowed = []
        self.startTime = None

    def listItems(self):
        return os.listdir('recordings')

    def write(self, string):
        if 'Store Timings' in self.allowed:
            timeString = '[{}] '.format(time.time()-self.startTime)
            string = timeString + string
        with open(self.path, 'a') as f:
            f.write(string + '\n')

    def remove(self, file):
        path = 'recordings/' + file
        if os.path.isfile(path):
            os.remove(path)

    def on_press(self, key):
        if key == self.killKey:
            return False
        if 'Keyboard' in self.allowed:
            self.write("KP {0}".format(key))

    def on_release(self, key):
        if 'Keyboard' in self.allowed:
            self.write("KR {0}".format(key))

    def on_move(self, x, y):
        if 'Mouse Movements' in self.allowed:
            self.write("MM ({0}, {1})".format(x, y))

    def on_click(self, x, y, button, pressed):
        if (('Left Button' in self.allowed) and button == pynput.mouse.Button.left) or (('Right Button' in self.allowed) and button == pynput.mouse.Button.right):
            if pressed:
                self.write('MP ({0}, {1}) {2}'.format(x, y, button))
            else:
                self.write('MR ({0}, {1}) {2}'.format(x, y, button))

    def on_scroll(self, x, y, dx, dy):
        if 'Scroll' in self.allowed:
            self.write('MS ({0}, {1})({2}, {3})'.format(x, y, dx, dy))


def replayRecording(file, logger):
    path = 'recordings/' + file
    if os.path.isfile(path):
        logger.debug('Replaying recording ' + path)
        startTime = time.time()
        keyboard = pynput.keyboard.Controller()
        mouse = pynput.mouse.Controller()
        with open(path, 'r') as f:
            lines = f.readlines()
            for i in range(len(lines)):
                line = lines[i].replace(' ', '')
                testSplit = line.split('[')
                if len(testSplit) != 1:
                    timeStr, line = testSplit[1].split(']')
                    while time.time()-startTime < float(timeStr):
                        time.sleep(0.001)
                cmd = line[:2]
                try:
                    if cmd[0] == 'K':
                        try:
                            key = line.split("'")[1]
                        except IndexError:
                            key = eval('pynput.keyboard.' + line[2:])
                        if cmd == 'KP':
                            keyboard.press(key)
                        elif cmd == 'KR':
                            keyboard.release(key)
                        else:
                            logger.warning("'{}' on line {} of {} is not a valid command, skipping.".format(cmd, i+1, path))
                    elif cmd[0] == 'M':
                        a = line.split('(') 
                        b = a[1].split(')') 
                        c = b[0].split(',')
                        d = [int(v) for v in c]
                        mouse.position = tuple(d)
                        if cmd == 'MP' or cmd == 'MR':
                            arg2 = b[1]
                            button = None
                            if arg2 == 'Button.left\n':
                                button = pynput.mouse.Button.left
                            elif arg2 == 'Button.right\n':
                                button = pynput.mouse.Button.right
                            else:
                                logger.warning("'{}' is not a valid mouse button. (line {} of {})".format(arg2, i+1, path))
                            if button:
                                if cmd == 'MP':
                                    mouse.press(button)
                                else:
                                    mouse.release(button)
                        elif cmd == 'MS':
                            e = a[2].split(')')
                            f = e[0].split(',')
                            g = [int(v) for v in f]
                            mouse.scroll(g[0], g[1])
                    else:
                        logger.warning("'{}' on line {} of {} is not a valid command, skipping.".format(cmd, i+1, path))
                except Exception as e:
                    logger.error('Error when running line {} of {}: {}'.format(i+1, path, e))
        logger.debug('Finished replaying recording ' + path)
    else:
        raise IOError(path + ' is not a file.')

class Recordings(LabelFrame):
    def __init__(self, parent, text, logger, root):
        super().__init__(parent, text=text)
        self.master = parent
        self.logger = logger
        self.root = root

        self.widgets = []

        self.addButton = Button(self, text='➕', command=self.add)
        self.addButton.grid(row=0, column=0)

        self.refreshButton = Button(self, text='Refresh', command=self.update)
        self.refreshButton.grid(row=0, column=1)

        self.recordingsFrame = gui.ScrollFrame(self, (400, 100))
        self.recordingsFrame.grid(row=1, column=0, columnspan=2)
        self.recordingsGrid = self.recordingsFrame.viewPort

        self.recordingsFile = RecordingsFile()

        self.updates = []

        self.update()

    def add(self):
        self.childWindow = Toplevel(self.master)
        self.childWindow.title('Name Recording')
        gui.GUI.setWindowIcon(self.childWindow)
        self.childWindow.geometry('250x263')
        label1 = Label(self.childWindow, text='Name')
        label1.pack()
        self.newRecordingName = Entry(self.childWindow)
        self.newRecordingName.pack(fill=X, expand=YES)
        label2 = Label(self.childWindow, text='Kill key')
        label2.pack()
        self.killKey = KeySelector(self.childWindow, self.root)
        self.killKey.pack(fill=X, expand=YES)
        self.types = CheckList(self.childWindow, ['Keyboard', 'Mouse Movements', 'Left Button', 'Right Button', 'Scroll', 'Store Timings'])
        self.types.pack(fill=X, expand=YES)
        createButton = Button(self.childWindow, text="Record", command=self.record)
        createButton.pack(fill=X, expand=YES)

    def confirmRemove(self, item):
        self.childWindow = Toplevel(self.master)
        self.childWindow.title('Confirm Remove')
        gui.GUI.setWindowIcon(self.childWindow)
        self.childWindow.geometry('250x60')
        createButton = Button(self.childWindow, text="Remove "+item, command=lambda: self.remove(item))
        createButton.pack(fill=X, expand=YES)
        cancelButton = Button(self.childWindow, text="Cancel", command=self.childWindow.destroy)
        cancelButton.pack(fill=X, expand=YES)

    def record(self):
        if self.killKey.get() == '':
            self.logger.error('Must set kill key for recording.')
        elif self.newRecordingName.get() == '':
            self.logger.error('Must set name for recording.')
        else:
            self.recordingsFile.killKey = self.killKey.key
            if not os.path.exists('recordings'):
                os.makedirs('recordings')
            self.recordingsFile.path = 'recordings/{}.txt'.format(self.newRecordingName.get())
            self.recordingsFile.allowed = self.types.get()
            self.recordingsFile.startTime = time.time()
            self.childWindow.destroy()
            self.logger.system('Recording started with kill key {}.'.format(self.killKey.get()))

            keyboardListener = pynput.keyboard.Listener(on_press=self.recordingsFile.on_press, 
                                                on_release=self.recordingsFile.on_release)
            mouseListener = pynput.mouse.Listener(on_move=self.recordingsFile.on_move, 
                                        on_click=self.recordingsFile.on_click, 
                                        on_scroll=self.recordingsFile.on_scroll)

            keyboardListener.start()
            mouseListener.start()
            while keyboardListener.is_alive():
                self.root.update()
            keyboardListener.join()
            mouseListener.stop()
            mouseListener.join()
            self.logger.system("Recording stopped and saved as '{}'.".format(self.recordingsFile.path))
            self.update()

    def update(self):
        for b,l,s,d in self.widgets:
            b.destroy()
            l.destroy()
            s.destroy()
            d.destroy()
        self.widgets = []
        
        fileList = self.recordingsFile.listItems()
        for i in range(len(fileList)):
            stats = os.stat('recordings/' + fileList[i])
            self.widgets.append(
                (   
                    Button(self.recordingsGrid, text='❌', command=lambda file=fileList[i]: self.confirmRemove(file)),
                    Label(self.recordingsGrid, text=fileList[i], width=30, anchor=W), 
                    Label(self.recordingsGrid, text=str(stats.st_size)+'B'), 
                    Label(self.recordingsGrid, text=datetime.fromtimestamp(stats.st_mtime).strftime("%d %B %Y %I:%M:%S"))
                )
            )
            self.widgets[i][0].grid(row=i, column=0)
            self.widgets[i][1].grid(row=i, column=1)
            self.widgets[i][2].grid(row=i, column=2)
            self.widgets[i][3].grid(row=i, column=3)

        for f in self.updates:
            f(fileList)

    def addUpdate(self, f):
        self.updates.append(f)
        self.update()

    def remove(self, item):
        self.childWindow.destroy()
        self.recordingsFile.remove(item)
        self.update()

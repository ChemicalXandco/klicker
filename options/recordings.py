import pynput
import os
import time
from tkinter import *

import gui
from options.utils import CheckList


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
        self.childWindow.geometry('250x250')
        label1 = Label(self.childWindow, text='Name')
        label1.pack()
        self.newRecordingName = Entry(self.childWindow)
        self.newRecordingName.pack(fill=X, expand=YES)
        label2 = Label(self.childWindow, text='Kill key')
        label2.pack()
        vcmd = (self.register(self.limitChar), '%i')
        self.killKey = Entry(self.childWindow, validate='key', validatecommand=vcmd)
        self.killKey.pack(fill=X, expand=YES)
        self.types = CheckList(self.childWindow, ['Keyboard', 'Mouse Movements', 'Left Button', 'Right Button', 'Scroll', 'Store Timings'])
        self.types.pack(fill=X, expand=YES)
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
            self.recordingsFile.allowed = self.types.get()
            self.recordingsFile.startTime = time.time()
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

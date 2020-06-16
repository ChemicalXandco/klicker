from tkinter import *
from tkinter.filedialog import askopenfilename
import logging
import uuid

from pynput import keyboard


class FileSelector(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.button = Button(self, text='Select File', command=self.getFilename)
        self.button.grid(row=0, column=0)
        self.path = Entry(self, width=35)
        self.path.grid(row=0, column=1)
        
    def getFilename(self):
        filename = askopenfilename()
        self.path.delete(0,END)
        self.path.insert(0, filename)


class KeySelector(Button):
    def __init__(self, parent, root, *args, **kwargs):
        kwargs['command'] = self.listen
        super().__init__(parent, *args, **kwargs)

        self.root = root
        self.key = None

        self.setText()

    def setText(self, text=''):
        if not text:
            text = 'Click to set a key'
        self.configure(text=text)

    def listen(self):
        with keyboard.Events() as events:
            event = None
            self.setText('Press a key')
            while not event:
                event = events.get(0.01)
                self.root.update()
        self.set(event.key)

    def get(self):
        if self.key == None:
            return ''
        if isinstance(self.key, keyboard.KeyCode):
            return self.key.char
        else:
            return str(self.key)

    def set(self, v):
        if isinstance(v, str):
            try:
                self.key = eval('keyboard.' + v)
            except AttributeError:
                self.key = keyboard.KeyCode(char=v)
            except SyntaxError:
                self.key = None
        else:
            self.key = v
        self.setText(self.get())


class OverlayWindow(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.wm_attributes("-topmost", 1)
        self.overrideredirect(1)


class CheckList(Frame):
    def __init__(self, parent, items=[], default=1):
        super().__init__(parent)

        self.items = []
        self.default = default
        self.vars = []
        self.buttons = []

        self.update(items)

    def update(self, items, updateTo=-1):
        newItems = {}
        for i in items:
            if i in self.items:
                if updateTo >= 0:
                    newItems[i] = updateTo
                else:
                    newItems[i] = self.vars[self.items.index(i)].get()
            else:
                newItems[i] = self.default
        self.items = items
        self.vars = []
        for b in self.buttons:
            b.destroy()
        self.buttons = []
        for k, v in newItems.items():
            index = len(self.vars)
            self.vars.append(IntVar())
            self.vars[index].set(v)
            self.buttons.append(Checkbutton(self, text=k, variable=self.vars[index]))
            self.buttons[index].pack(anchor=W)

    def get(self):
        checked = []
        for i in range(len(self.items)):
            if self.vars[i].get() == 1:
                checked.append(self.items[i])
        return checked


def levelStrToColour(level):
    if level == 'WARNING':
        return 'orange'
    elif level == 'ERROR':
        return 'red'
    elif level == 'SYSTEM':
        return 'blue'
    else:
        return 'black'


class DeactivateRequest(Exception):
    pass


class TextHandler(logging.Handler):
    # from https://gist.github.com/moshekaplan/c425f861de7bbf28ef06
    """This class allows you to log to a Tkinter Text or ScrolledText widget"""
    def __init__(self, text):
        # run the regular Handler __init__
        logging.Handler.__init__(self)
        # Store a reference to the Text it will log to
        self.text = text

    def emit(self, record):
        msg = self.format(record)
        def append():
            self.text.configure(state='normal')
            startIndex = self.text.index(INSERT)
            self.text.insert(END, msg + '\n')
            level = (msg.split('['))[2].split(']')[0]
            tempUuid = str(uuid.uuid4()) # Tempory uuid to avoid conflicts between tags
            self.text.tag_add(tempUuid, startIndex, END)
            self.text.tag_config(tempUuid, foreground=levelStrToColour(level))
            # Autoscroll to the bottom
            self.text.yview(END)
            self.text.configure(state='disabled')
        append()

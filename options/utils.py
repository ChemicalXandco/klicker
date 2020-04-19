from tkinter import *
from tkinter.filedialog import askopenfilename
import logging
import uuid


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


class OverlayWindow(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.wm_attributes("-topmost", 1)
        self.overrideredirect(1)


def levelStrToColour(level):
    if level == 'WARNING':
        return 'orange'
    if level == 'ERROR':
        return 'red'
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

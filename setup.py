import sys, os, platform
from cx_Freeze import setup, Executable

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

base = None
name = None
bdist_msi_options = None
if sys.platform == 'win32':
    base = 'Win32GUI'
    name = 'Simple Clicker.exe'
    shortcut_table = [
        ('DesktopShortcut',        # Shortcut
         'DesktopFolder',          # Directory_
         'Simple Clicker',         # Name
         'TARGETDIR',              # Component_
         '[TARGETDIR]'+name,       # Target
         None,                     # Arguments
         'a simple clicker tool to click quickly/constantly',# Description
         None,                     # Hotkey
         None,                     # Icon
         None,                     # IconIndex
         None,                     # ShowCmd
         'TARGETDIR'               # WkDir
         )]
    msi_data = {"Shortcut": shortcut_table}
    bdist_msi_options = {'data': msi_data}
    
opts = {'include_files':['config.ini', 'LICENSE', 'README.MD',
                         'icon.ico', 'profiles.json',
                         (os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'), os.path.join('lib', 'tcl86t.dll')),
                         (os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'), os.path.join('lib', 'tk86t.dll'))]}

setup(  name = 'Simple Clicker',
        version = '2.1',
        description = 'Easily create complex macros.',
        options = {'build_exe': opts, "bdist_msi": bdist_msi_options},
        executables = [Executable('main.py', targetName=name,
                                  icon='icon.ico',
                                  base=base)])

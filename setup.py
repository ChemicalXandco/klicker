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
    name = 'Klicker.exe'
    shortcut_table = [
        ('DesktopShortcut',        # Shortcut
         'DesktopFolder',          # Directory_
         'Klicker',                # Name
         'TARGETDIR',              # Component_
         '[TARGETDIR]'+name,       # Target
         None,                     # Arguments
         'A python GUI application for automating the keyboard and mouse.',# Description
         None,                     # Hotkey
         None,                     # Icon
         None,                     # IconIndex
         None,                     # ShowCmd
         'TARGETDIR'               # WkDir
         )]
    msi_data = {"Shortcut": shortcut_table}
    bdist_msi_options = {'data': msi_data}

opts = {
    # include dynamically loaded options
    'packages': [
        'options.boolean',
        'options.nonsequential',
        'options.sequential',
    ],
    'include_files': [
        'config.ini', 'LICENSE', 'README.MD', 'icon.ico',
        (os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'), os.path.join('lib', 'tcl86t.dll')),
        (os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'), os.path.join('lib', 'tk86t.dll')),
    ],
}

setup(  name = 'Klicker',
        version = '3.0',
        description = 'A python GUI application for automating the keyboard and mouse.',
        options = {'build_exe': opts, "bdist_msi": bdist_msi_options},
        executables = [Executable('main.py', targetName=name,
                                  icon='icon.ico',
                                  base=base)])

# <img src="icon.png" width="32" height="32"> Klicker

A python GUI application for automating the keyboard and mouse.

# Download the latest binary [here](https://github.com/ChemicalXandco/klicker/releases)

or...

# Install & set up

You must have python 3 installed
To get the required modules run `pip3 install -r requirements.txt`

In order to start the application, run `python3 main.py`.

### Linux install

Install the following:

`sudo apt-get install scrot`,
`sudo apt-get install python3-tk`,
`sudo apt-get install python3-dev`

then run `sudo python3 main.py`

# Usage

A hotkey is setup to trigger the clicker, default is `x`.
A default profile is stored along with this that will be loaded at the start. It can be set by selecting the profile you want and then saving the configuration.

The configuration is stored in the file `config.ini` and can be saved and reloaded using the `Save Configuration` and `Refresh Configuration` buttons respectively. The file stores the hotkey, the name of the profile and the log level.

Options can be added by clicking on the drop-down menu and removed by clicking on the cross next to the option

The log file is cleared on every startup, it can also be cleared by pressing the `Clear Log` button. Only the messages higher or equal to the current log level will be logged.

### Profile Usage

Profiles store options so that they can easily be used later.

Profiles can be created by clicking on the plus symbol in the 'Profile' panel. A window will appear and you type the name of the profile and click `Create`, then all the options that are currently set will be written to a profile of that name.

To delete a profile, select the one you want to delete and click the cross, then confirm deletion.

### Number Usage

Any option that takes a number as an input can have calculations and functions. Variables can be set in the 'Numbers' panel and used in the number entry. Additionally, the following variables can be used:

- Constants from the python `math` library such as `pi` (written exactly like that)
- `counter`: a value that increases by 1 every time the number is parsed
- `timer`: the time in seconds since the state resetted

The following functions can be used:
- Standard python built-in functions such as `round()` and `abs()`
- `cache()`: keep the same value for each time it is parsed, for example `cache(randint(1, 10))` will always be whatever is selected at random until the state resets, then another number will be chosen
- Functions from the python `math` library such as `cos()` (written exactly like that)
- Functions from the python `random` library such as `randint()` (written exactly like that)
- `randfloat()` instead of the `random` library's `uniform()`

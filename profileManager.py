import json

def read():
    try:
        with open('profiles.json', 'r') as file:
            parsed = json.load(file)
    except FileNotFoundError:
        parsed = {}
    return parsed

def write(profileName, profile):
    changes = read()
    changes[profileName] = profile
    with open('profiles.json', 'w') as file:
        json.dump(changes, file, indent=4)

def remove(profileName):
    changes = read()
    changes.pop(profileName)
    with open('profiles.json', 'w') as file:
        json.dump(changes, file, indent=4)

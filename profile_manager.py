import json

def read():
    file = open('profiles.json', 'r')
    parsed = json.load(file)
    file.close()
    return parsed

def write(profileName, profile):
    changes = read()

    changes[profileName] = {}
    
    for option, attributes in profile.items():
        changes[profileName][option] = {}
        for attribute, value in attributes.items():
            changes[profileName][option][attribute] = value
    
    file = open('profiles.json', 'w')
    json.dump(changes, file, indent=4)
    file.close()

def remove(profileName):
    changes = read()

    changes.pop(profileName)

    file = open('profiles.json', 'w')
    json.dump(changes, file, indent=4)
    file.close()
    

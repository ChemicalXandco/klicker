import json

def read():
    file = open('profiles.json', 'r')
    parsed = json.load(file)
    file.close()
    return parsed

def write(profileName, profile):
    changes = read()

    changes[profileName] = profile
    
    file = open('profiles.json', 'w')
    json.dump(changes, file, indent=4)
    file.close()

def remove(profileName):
    changes = read()

    changes.pop(profileName)

    file = open('profiles.json', 'w')
    json.dump(changes, file, indent=4)
    file.close()
    

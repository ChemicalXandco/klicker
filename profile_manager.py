import json

class Profiles:
    def write(profileName, profile):
        changes = Profiles.read()

        print(str(changes))

        if not profileName in changes:
            changes[profileName] = {}
        
        for option, attributes in profile.items():
            if not option in changes[profileName]:
                changes[profileName][option] = {}
            for attribute, value in attributes.items():
                changes[profileName][option][attribute] = value
                 

        file = open('profiles.json', 'w')
        json.dump(changes, file)
        file.close()

    def read():
        file = open('profiles.json', 'r')
        parsed = json.load(file)
        file.close()
        return parsed

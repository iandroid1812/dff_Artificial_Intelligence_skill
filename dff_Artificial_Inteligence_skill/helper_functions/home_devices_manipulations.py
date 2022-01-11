import ruamel.yaml
import re

yaml = ruamel.yaml.YAML()


def lights_manipulations(todo: str, room: str):
    with open('home_devices/light_groups.yaml') as f:
        data = yaml.load(f)
    for group in data:
        if bool(re.compile(room, re.I).search(group['name'])):
            for light in group['entities']:
                key = list(light.keys())[0]
                # check if the light is dimmable
                if not bool(re.compile(r'dimmable', re.I).search(key)):
                    light[key] = todo
                else:
                    # full brightness if turning on
                    light[key] = 100 if todo == 'on' else 0
    with open('home_devices/light_groups.yaml', 'w') as f:
        yaml.dump(data, f)


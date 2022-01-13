import ruamel.yaml
import re

yaml = ruamel.yaml.YAML()


def lights_manipulations(todo: str, room: str):
    with open('home_devices/light_groups.yaml') as f:
        data = yaml.load(f)
    changes = False
    for group in data:
        if bool(re.compile(room, re.I).search(group['name'])):
            for light in group['entities']:
                key = list(light.keys())[0]
                # check if the light is dimmable
                if not bool(re.compile(r'dimmable', re.I).search(key)):
                    light[key] = todo
                    changes = True
                else:
                    # full brightness if turning on
                    light[key] = 100 if todo == 'on' else 0
                    changes = True
    if changes:
        with open('home_devices/light_groups.yaml', 'w') as f:
            yaml.dump(data, f)


def dimmable_lights_manipulations(todo: int, room: str, check=False):
    with open('home_devices/light_groups.yaml') as f:
        data = yaml.load(f)
    changes = False
    for group in data:
        if bool(re.compile(room, re.I).search(group['name'])):
            for light in group['entities']:
                key = list(light.keys())[0]
                # check if the light is dimmable
                if bool(re.compile(r'dimmable', re.I).search(key)) and not check:
                    light[key] = todo
                    changes = True
                elif bool(re.compile(r'dimmable', re.I).search(key)) and check:
                    return True
    if changes:
        with open('home_devices/light_groups.yaml', 'w') as f:
            yaml.dump(data, f)
    if check:
        return False


def set_the_temp(todo: int, room: str):
    with open('home_devices/climate_group.yaml') as f:
        data = yaml.load(f)
    changes = False
    for group in data:
        if bool(re.compile(room, re.I).search(group['name'])):
            for temp in group['entities']:
                key = list(temp.keys())[0]
                temp[key] = todo
                changes = True
    if changes:
        with open('home_devices/climate_group.yaml', 'w') as f:
            yaml.dump(data, f)


def heat_up_the_temp(room: str):
    with open('home_devices/climate_group.yaml') as f1:
        data = yaml.load(f1)
    with open('home_devices/temperature_sensors.yaml') as f2:
        sensors = yaml.load(f2)

    changes = False
    cur_temp = None
    for area in sensors:
        if bool(re.compile(room, re.I).search(area['name'])):
            cur_temp = int(area['temperature'])

    if cur_temp is None:
        return "Unavailable"

    for group in data:
        if bool(re.compile(room, re.I).search(group['name'])):
            for temp in group['entities']:
                key = list(temp.keys())[0]
                temp[key] = cur_temp + 10
                changes = True

    if changes:
        with open('home_devices/climate_group.yaml', 'w') as f:
            yaml.dump(data, f)

    return cur_temp + 10

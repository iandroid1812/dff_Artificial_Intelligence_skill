import re
import ruamel.yaml
from typing import Optional

yaml = ruamel.yaml.YAML()


def lights_manipulations(room: Optional[str] = None, todo: Optional[str] = None):
    if room is None and todo is None:
        return
    with open('home_devices/light_groups.yaml') as f:
        data = yaml.load(f)
    changes = False
    for group in data:
        if bool(re.compile(room, re.I).search(group['name'])) or room == 'all':
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


def dimmable_lights_manipulations(room: Optional[str] = None, todo: Optional[int] = None):
    if room is None and todo is None:
        return
    with open('home_devices/light_groups.yaml') as f:
        data = yaml.load(f)
    changes = False
    for group in data:
        if bool(re.compile(room, re.I).search(group['name'])):
            for light in group['entities']:
                key = list(light.keys())[0]
                # check if the light is dimmable
                if bool(re.compile(r'dimmable', re.I).search(key)):
                    if todo is None:
                        return True
                    light[key] = todo
                    changes = True
    if todo is None:
        return False
    if changes:
        with open('home_devices/light_groups.yaml', 'w') as f:
            yaml.dump(data, f)


def check_dimmable(room) -> bool:
    return dimmable_lights_manipulations(room=room) if room else False


def set_the_temp(room: Optional[str] = None, todo: Optional[int] = None):
    if room is None and todo is None:
        return
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


def heat_cool_the_temp(room: Optional[str] = None, todo: Optional[str] = None):
    if room is None:
        return "Unavailable"
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
                temp[key] = cur_temp + 10 if todo == "heat" else cur_temp - 10
                changes = True

    if changes:
        with open('home_devices/climate_group.yaml', 'w') as f:
            yaml.dump(data, f)

    return cur_temp + 10 if todo == "heat" else cur_temp - 10


def heat_floor(room: Optional[str] = None):
    if room is None:
        return
    with open('home_devices/climate_group.yaml') as f:
        data = yaml.load(f)

    for group in data:
        if bool(re.compile(room, re.I).search(group['name'])):
            for temp in group['entities']:
                key = list(temp.keys())[0]
                temp[key] += 20

    with open('home_devices/climate_group.yaml', 'w') as f:
        yaml.dump(data, f)

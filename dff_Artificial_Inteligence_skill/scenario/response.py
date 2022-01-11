# for responses
# TODO: add responses

import re
from df_engine.core import Actor, Context
from helper_functions.requesting import weather_forecast_request
from helper_functions.home_devices_manipulations import lights_manipulations


def basic_weather_response(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    if "weather_forecast" not in ctx.misc.keys():
        ctx.misc['weather_forecast'] = weather_forecast_request()

    degree = u'\N{DEGREE SIGN}'
    loc = ctx.misc['weather_forecast']['loc']
    temp = ctx.misc['weather_forecast']['temp']
    feel = ctx.misc['weather_forecast']['feels-like']

    forecast = f"The temperature in {loc} is {temp}{degree}C. It feels like " \
               f"{feel}{degree}C.\nDo you want to get more information?"
    return forecast


def extra_weather_response(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    if "weather_forecast" not in ctx.misc.keys():
        return ""

    report = ctx.misc['weather_forecast']['report']
    hum = ctx.misc['weather_forecast']['humidity']
    wind = ctx.misc['weather_forecast']['wind']

    forecast = f"Weather report: {report}. The humidity level is {hum}% and the wind speed is {wind} m/s."
    return forecast


def light_response(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    room_pattern = re.compile(r'\bhall\b|\bliving room\b|\bkitchen\b|\bbedroom\b', re.I)
    try:
        room = room_pattern.search(ctx.last_request)[0]
        print(room)
        lights_manipulations(ctx.misc['light_action'], room)
        response = f"Turned {ctx.misc['light_action']} the lights in the {room}"
    except TypeError:
        response = ""

    return response

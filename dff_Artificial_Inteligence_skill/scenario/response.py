# for responses
# TODO: add responses

import re
from df_engine.core import Actor, Context
from googletrans import Translator
from helper_functions.requesting import weather_forecast_request
from helper_functions.home_devices_manipulations import lights_manipulations, \
    dimmable_lights_manipulations, set_the_temp, heat_up_the_temp


def response_translate(ctx: Context, response: str) -> str:
    # current_lang = ctx.misc.get('lang')
    # if current_lang == 'ENG':
    #     return response
    # elif current_lang == 'RUS':
    #     translator = Translator()
    #     translation = translator.translate(response, dest="ru")
    #     return translation
    return response


def basic_weather_response(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    if "weather_forecast" not in ctx.misc.keys():
        ctx.misc['weather_forecast'] = weather_forecast_request()

    degree = u'\N{DEGREE SIGN}'
    loc = ctx.misc['weather_forecast']['loc']
    temp = ctx.misc['weather_forecast']['temp']
    feel = ctx.misc['weather_forecast']['feels-like']

    forecast = f"The temperature in {loc} is {temp}{degree}C. It feels like " \
               f"{feel}{degree}C.\nDo you want to get more information?"
    return response_translate(ctx, forecast)


def extra_weather_response(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    if "weather_forecast" not in ctx.misc.keys():
        return ""

    report = ctx.misc['weather_forecast']['report']
    hum = ctx.misc['weather_forecast']['humidity']
    wind = ctx.misc['weather_forecast']['wind']

    forecast = f"Weather report: {report}. The humidity level is {hum}% and the wind speed is {wind} m/s."
    return response_translate(ctx, forecast)


def light_response(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    try:
        lights_manipulations(ctx.misc['light_action'], ctx.misc['room'])
        response = f"Turned {ctx.misc['light_action']} the lights in the {ctx.misc['room']}"
    except (TypeError, KeyError):
        response = ""
    return response_translate(ctx, response)


def dim_response(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    try:
        dimmable_lights_manipulations(todo=ctx.misc['percentage'], room=ctx.misc['room'])
        response = f"Dimmed the light in the {ctx.misc['room']} to {ctx.misc['percentage']}%"
    except (TypeError, KeyError):
        response = ""
    return response_translate(ctx, response)


def no_dim(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    try:
        response = f"I am certain that {ctx.misc['room']} has no dimmable lights available."
    except (TypeError, KeyError):
        response = ""
    return response_translate(ctx, response)


def temperature_setting(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    try:
        set_the_temp(todo=ctx.misc['temperature'], room=ctx.misc['room'])
        response = f"Set the temperature in the {ctx.misc['room']} to {ctx.misc['temperature']} degrees"
    except (TypeError, KeyError):
        response = ""
    return response_translate(ctx, response)


def heating_up(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    try:
        target = heat_up_the_temp(room=ctx.misc['room'])
        if target == "Unavailable":
            response = "Could not heat up the room, there are no sensors available to measure current temperature"
        else:
            response = f"Set the climate system to heat up the {ctx.misc['room']} to {target} degrees"
    except (TypeError, KeyError):
        response = ""
    return response_translate(ctx, response)


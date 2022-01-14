# for responses
# TODO: add responses

import re
from df_engine.core import Actor, Context
from deep_translator import GoogleTranslator as Translator
from helper_functions.requesting import weather_forecast_request
from helper_functions.translator import translate
from helper_functions.home_devices_manipulations import lights_manipulations, \
    dimmable_lights_manipulations, set_the_temp, heat_cool_the_temp


def response_translate(ctx: Context, response: str) -> str:
    current_lang = ctx.misc.get('lang')
    if current_lang == 'RUS':
        translator = Translator(target='ru')
        translation = translator.translate(response)
        return translation
    return response


def awaiting(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    response = "Awaiting for commands..."
    return translate(ctx.misc.get('lang'), response, option='response')


def language_change(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    response = f"Language change successful"
    return translate(ctx.misc.get('lang'), response, option='response')


def fallback(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    response = "I didn't quite catch that, can you repeat please?"
    return translate(ctx.misc.get('lang'), response, option='response')


def greet(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    response = "Hello, I am your Home Assistant. How can I help?"
    return translate(ctx.misc.get('lang'), response, option='response')


def negative_weather(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    response = "Ok, that's it for the weather then."
    return translate(ctx.misc.get('lang'), response, option='response')


def which_room(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    response = "Ok, in which room?"
    return translate(ctx.misc.get('lang'), response, option='response')


def want_dim(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    response = "Do you want to dim the light as well?"
    return translate(ctx.misc.get('lang'), response, option='response')


def which_dim(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    response = "Alright, in which room do I need to dim the light?"
    return translate(ctx.misc.get('lang'), response, option='response')


def brightness(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    response = "What brightness do you want?"
    return translate(ctx.misc.get('lang'), response, option='response')


def appreciate(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    response = "Glad I could help!"
    return translate(ctx.misc.get('lang'), response, option='response')


def basic_weather_response(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    if "weather_forecast" not in ctx.misc.keys():
        ctx.misc['weather_forecast'] = weather_forecast_request()

    degree = u'\N{DEGREE SIGN}'
    loc = ctx.misc['weather_forecast']['loc']
    temp = ctx.misc['weather_forecast']['temp']
    feel = ctx.misc['weather_forecast']['feels-like']

    forecast = f"The temperature in {loc} is {temp}{degree}C. It feels like " \
               f"{feel}{degree}C.\nDo you want to get more information?"
    return translate(ctx.misc.get('lang'), forecast, option='response')


def extra_weather_response(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    if "weather_forecast" not in ctx.misc.keys():
        return ""

    report = ctx.misc['weather_forecast']['report']
    hum = ctx.misc['weather_forecast']['humidity']
    wind = ctx.misc['weather_forecast']['wind']

    forecast = f"Weather report: {report}. The humidity level is {hum}% and the wind speed is {wind} m/s."
    return translate(ctx.misc.get('lang'), forecast, option='response')


def light_response(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    try:
        lights_manipulations(ctx.misc['light_action'], ctx.misc['room'])
        response = f"Turned {ctx.misc['light_action']} the lights in the {ctx.misc['room']}"
    except (TypeError, KeyError):
        response = ""
    return translate(ctx.misc.get('lang'), response, option='response')


def dim_response(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    try:
        dimmable_lights_manipulations(todo=ctx.misc['percentage'], room=ctx.misc['room'])
        response = f"Dimmed the light in the {ctx.misc['room']} to {ctx.misc['percentage']}%"
    except (TypeError, KeyError):
        response = ""
    return translate(ctx.misc.get('lang'), response, option='response')


def no_dim(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    try:
        response = f"I am certain that {ctx.misc['room']} has no dimmable lights available."
    except (TypeError, KeyError):
        response = ""
    return translate(ctx.misc.get('lang'), response, option='response')


def temperature_setting(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    try:
        set_the_temp(todo=ctx.misc['temperature'], room=ctx.misc['room'])
        response = f"The temperature in the {ctx.misc['room']} was set to {ctx.misc['temperature']} degrees"
    except (TypeError, KeyError):
        response = ""
    return translate(ctx.misc.get('lang'), response, option='response')


def heating_up(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    try:
        target = heat_cool_the_temp(todo='heat', room=ctx.misc['room'])
        if target == "Unavailable":
            response = "Could not heat up the room, there are no sensors available to measure current temperature"
        else:
            response = f"Climate system was set to heat up the {ctx.misc['room']} to {target} degrees"
    except (TypeError, KeyError):
        response = ""
    return translate(ctx.misc.get('lang'), response, option='response')


def cooling_down(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    try:
        target = heat_cool_the_temp(todo='cool', room=ctx.misc['room'])
        if target == "Unavailable":
            response = "Could not cool down the room, there are no sensors available to measure current temperature"
        else:
            response = f"Climate system was set to cool down the {ctx.misc['room']} to {target} degrees"
    except (TypeError, KeyError):
        response = ""
    return translate(ctx.misc.get('lang'), response, option='response')


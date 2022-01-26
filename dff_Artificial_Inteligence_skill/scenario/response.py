import scenario.condition as loc_cnd
from annotators.main import annotate
from df_engine.core import Actor, Context
from helper_functions.requesting import weather_forecast_request
from helper_functions.translator_tts import translate, text_to_speech
from helper_functions.simple_Q_A import q_a_bot
import helper_functions.home_devices_manipulations as home


def main_response(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    """
    Checking for multiple conditions inside starting node and returning appropriate responses
    These conditions/responses are all grouped up in the same function because they do not lead to any other node,
    and if the condition is met we  still stay at the starting node.
    We just need to have custom responses for some of them.
    """
    if loc_cnd.lang_condition(ctx, actor):
        response = "Language change successful"
    elif loc_cnd.appreciate_condition(ctx, actor):
        response = "Glad I could help!"
    elif loc_cnd.greeting_condition(ctx, actor):
        response = "Hi, I am your Home Assistant. How can I help?"
    elif loc_cnd.goodbye_condition(ctx, actor):
        response = "Nice talking to you, goodbye"
    elif loc_cnd.tts_check(ctx, actor):
        var = 'enabled' if ctx.misc['tts'] else 'disabled'
        response = f"The TTS functionality was {var} successfully!"
    else:
        response = "I'm waiting for the command..."

    # translation of the response
    response = translate(ctx.misc.get('lang'), response, option='response')
    # calling tts to launch audio
    text_to_speech(response, ctx.misc.get('lang'), ctx.validation, ctx.misc.get('tts'))
    return response


def convo_stopped(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    response = "The conversation has been stopped. In order to begin say: 'start'."
    response = translate(ctx.misc.get('lang'), response, option='response')
    text_to_speech(response, ctx.misc.get('lang'), ctx.validation, ctx.misc.get('tts'))
    return response


def fallback(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    response = "Sorry, I didn't quite catch that. Can we try again?"
    response = translate(ctx.misc.get('lang'), response, option='response')
    text_to_speech(response, ctx.misc.get('lang'), ctx.validation, ctx.misc.get('tts'))
    return response


def which_room(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    response = "Ok, in which room?"
    response = translate(ctx.misc.get('lang'), response, option='response')
    text_to_speech(response, ctx.misc.get('lang'), ctx.validation, ctx.misc.get('tts'))
    return response


def questioning(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    prev = ctx.a_s.get('previous_label')
    if prev is not None:
        if prev[:2] != ('service_flow', 'Q&A'):
            response = "Ok, ask me."
        else:
            additional = "\nAnything else?"
            request = ctx.misc.get('translated') if ctx.misc.get('translated') is not None else ''
            response = q_a_bot(request) + additional
        response = translate(ctx.misc.get('lang'), response, option='response')
        return response


# ---------------- Weather responses ----------------

def basic_weather_response(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    ctx.misc['weather_forecast'] = weather_forecast_request()

    degree = u'\N{DEGREE SIGN}'
    loc = ctx.misc['weather_forecast']['loc']
    temp = ctx.misc['weather_forecast']['temp']
    feel = ctx.misc['weather_forecast']['feels-like']

    forecast = f"The temperature in {loc} is {temp}{degree}C. It feels like " \
               f"{feel}{degree}C.\nDo you want to get more information?"
    forecast = translate(ctx.misc.get('lang'), forecast, option='response')
    text_to_speech(forecast, ctx.misc.get('lang'), ctx.validation, ctx.misc.get('tts'))
    return forecast


def extra_weather_response(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    report = ctx.misc['weather_forecast']['report']
    hum = ctx.misc['weather_forecast']['humidity']
    wind = ctx.misc['weather_forecast']['wind']

    forecast = f"Weather report: {report}. The humidity level is {hum}% and the wind speed is {wind} m/s."
    forecast = translate(ctx.misc.get('lang'), forecast, option='response')
    text_to_speech(forecast, ctx.misc.get('lang'), ctx.validation, ctx.misc.get('tts'))
    return forecast


def negative_weather(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    response = "Ok, that's it for the weather then. Anything else?"
    response = translate(ctx.misc.get('lang'), response, option='response')
    text_to_speech(response, ctx.misc.get('lang'), ctx.validation, ctx.misc.get('tts'))
    return response


# ---------------- Light responses ----------------

def light_response(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    ctx = annotate(ctx) if ctx.validation else ctx
    home.lights_manipulations(room=ctx.misc['room'], todo=ctx.misc['light_action'])
    additional = "\nDo you want to dim the light as well?" if ctx.misc.get('dimmable') else "\nIs that all?"
    response = f"Turned {ctx.misc['light_action']} the lights in the {ctx.misc['room']}." + additional
    response = translate(ctx.misc.get('lang'), response, option='response')
    text_to_speech(response, ctx.misc.get('lang'), ctx.validation, ctx.misc.get('tts'))
    return response


def dim_response(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    ctx = annotate(ctx) if ctx.validation else ctx
    home.dimmable_lights_manipulations(room=ctx.misc['room'], todo=ctx.misc['percentage'])
    response = f"Dimmed the light in the {ctx.misc['room']} to {ctx.misc['percentage']}%"
    response = translate(ctx.misc.get('lang'), response, option='response')
    text_to_speech(response, ctx.misc.get('lang'), ctx.validation, ctx.misc.get('tts'))
    return response


def want_dim(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    response = "Do you want to dim the light as well?"
    response = translate(ctx.misc.get('lang'), response, option='response')
    text_to_speech(response, ctx.misc.get('lang'), ctx.validation, ctx.misc.get('tts'))
    return response


def which_dim(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    response = "Alright, in which room do I need to dim the light?"
    response = translate(ctx.misc.get('lang'), response, option='response')
    text_to_speech(response, ctx.misc.get('lang'), ctx.validation, ctx.misc.get('tts'))
    return response


def brightness(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    response = "What brightness do you want?"
    response = translate(ctx.misc.get('lang'), response, option='response')
    text_to_speech(response, ctx.misc.get('lang'), ctx.validation, ctx.misc.get('tts'))
    return response


def no_dim(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    ctx = annotate(ctx) if ctx.validation else ctx
    response = f"I am certain that {ctx.misc['room']} has no dimmable lights available.\n" \
               f"Want to try another room?"
    response = translate(ctx.misc.get('lang'), response, option='response')
    text_to_speech(response, ctx.misc.get('lang'), ctx.validation, ctx.misc.get('tts'))
    return response


# ---------------- Temperature responses ----------------

def temperature_setting(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    ctx = annotate(ctx) if ctx.validation else ctx
    home.set_the_temp(room=ctx.misc['room'], todo=ctx.misc['temperature'])
    response = f"The temperature in the {ctx.misc['room']} was set to {ctx.misc['temperature']} degrees"
    response = translate(ctx.misc.get('lang'), response, option='response')
    text_to_speech(response, ctx.misc.get('lang'), ctx.validation, ctx.misc.get('tts'))
    return response


def heating_up(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    ctx = annotate(ctx) if ctx.validation else ctx
    target = home.heat_cool_the_temp(room=ctx.misc['room'], todo='heat')
    if target == "Unavailable":
        response = f"Could not heat up the {ctx.misc['room']}, there are no sensors " \
                   "available to measure current temperature"
    else:
        response = f"Climate system was set to heat up the {ctx.misc['room']} to {target} degrees"
    response = translate(ctx.misc.get('lang'), response, option='response')
    text_to_speech(response, ctx.misc.get('lang'), ctx.validation, ctx.misc.get('tts'))
    return response


def cooling_down(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    ctx = annotate(ctx) if ctx.validation else ctx
    target = home.heat_cool_the_temp(room=ctx.misc['room'], todo='cool')
    if target == "Unavailable":
        response = f"Could not cool down the {ctx.misc['room']}, there are no sensors " \
                   f"available to measure current temperature"
    else:
        response = f"Climate system was set to cool down the {ctx.misc['room']} to {target} degrees"
    response = translate(ctx.misc.get('lang'), response, option='response')
    text_to_speech(response, ctx.misc.get('lang'), ctx.validation, ctx.misc.get('tts'))
    return response


def floor_heat(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    ctx = annotate(ctx) if ctx.validation else ctx
    home.lights_manipulations(room='all', todo='off')
    response = "Turned on the floor heating in the hall. See you at home!"
    response = translate(ctx.misc.get('lang'), response, option='response')
    text_to_speech(response, ctx.misc.get('lang'), ctx.validation, ctx.misc.get('tts'))
    return response


# ---------------- Presence scenarios responses ----------------

def going_away(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    ctx = annotate(ctx) if ctx.validation else ctx
    ctx.misc['weather_forecast'] = weather_forecast_request()
    if ctx.misc['weather_forecast']['report'] in {'Rain', 'Snow'}:
        additional = 'Looks like there will be precipitations, choose your clothes wisely.\n'
    else:
        additional = ""
    response = additional + "Is there anyone else at home still?"
    response = translate(ctx.misc.get('lang'), response, option='response')
    text_to_speech(response, ctx.misc.get('lang'), ctx.validation, ctx.misc.get('tts'))
    return response


def getting_in(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    ctx = annotate(ctx) if ctx.validation else ctx
    ctx.misc['weather_forecast'] = weather_forecast_request()
    if ctx.misc['weather_forecast']['report'] in {'Rain', 'Snow'}:
        additional = '\nShould I heat up the floors in the hall, so everything dries up quickly?'
    else:
        additional = ""
    response = "Ok, see you at home." + additional
    response = translate(ctx.misc.get('lang'), response, option='response')
    text_to_speech(response, ctx.misc.get('lang'), ctx.validation, ctx.misc.get('tts'))
    return response


def should(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    ctx = annotate(ctx) if ctx.validation else ctx
    response = "Should I check if the lights are turned off?."
    response = translate(ctx.misc.get('lang'), response, option='response')
    text_to_speech(response, ctx.misc.get('lang'), ctx.validation, ctx.misc.get('tts'))
    return response


def light_check(ctx: Context, actor: Actor, *args, **kwargs) -> str:
    ctx = annotate(ctx) if ctx.validation else ctx
    home.lights_manipulations(room='all', todo='off')
    response = "Turned off all the lights in each room. Goodbye, see you later!"
    response = translate(ctx.misc.get('lang'), response, option='response')
    text_to_speech(response, ctx.misc.get('lang'), ctx.validation, ctx.misc.get('tts'))
    return response

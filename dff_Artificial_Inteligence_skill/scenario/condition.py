# for conditions
# TODO: add conditions

import logging
import re
from googletrans import Translator
from df_engine.core import Actor, Context
from helper_functions.home_devices_manipulations import dimmable_lights_manipulations

logger = logging.getLogger(__name__)


def request_translate(ctx: Context) -> str:
    # request = ctx.last_request
    # current_lang = ctx.misc.get('lang')
    # if current_lang == 'ENG':
    #     return request
    # elif current_lang == 'RUS':
    #     translator = Translator()
    #     translation = translator.translate(request, dest="ru")
    #     return translation
    return ctx.last_request


# re patterns for the functions below
weather_pattern = re.compile(r'(what|\btell\b).*\bweather\b', re.I)
greeting_pattern = re.compile(r'\bhi|hello|hey\b', re.I)
appreciate_pattern = re.compile(r'thank|\bgood\b|\bnice\b', re.I)
light_pattern = re.compile(r'(turn\s)(off|on)(.*light+)', re.I)
dimming_pattern = re.compile(r'(dim)(.*light+)', re.I)
setting_temp_pattern = re.compile(r'(\bset\b).*(\btemperature\b).*(\bto\b)', re.I)
heating_pattern = re.compile(r'(\bheat\b)', re.I)


def greeting_condition(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    request = request_translate(ctx)
    return bool(greeting_pattern.search(request))


def weather_condition(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    request = request_translate(ctx)
    return bool(weather_pattern.search(request))


def condition_yes(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    return ctx.misc.get('binary_intent') == "yes"


def condition_no(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    return ctx.misc.get('binary_intent') == "no"


def appreciate_condition(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    request = request_translate(ctx)
    return bool(appreciate_pattern.search(request))


def room_condition(ctx: Context, actor: Actor) -> bool:
    request = request_translate(ctx)
    return bool(ctx.misc.get('room'))


def light_condition(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    request = request_translate(ctx)
    return bool(light_pattern.search(request))


def dim_condition(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    request = request_translate(ctx)
    return bool(dimming_pattern.search(request))


def check_dimmable(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    request = request_translate(ctx)
    if ctx.misc.get('room') is None:
        return False
    return dimmable_lights_manipulations(todo=0, room=ctx.misc.get('room'), check=True)


def get_brightness(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    request = request_translate(ctx)
    return bool(ctx.misc.get('percentage'))


def setting_temp_condition(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    request = request_translate(ctx)
    return bool(setting_temp_pattern.search(request))


def heating_condition(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    request = request_translate(ctx)
    return bool(heating_pattern.search(request))

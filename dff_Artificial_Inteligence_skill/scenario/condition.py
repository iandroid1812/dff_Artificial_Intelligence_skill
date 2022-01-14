import logging
import re
from deep_translator import GoogleTranslator as Translator
from df_engine.core import Actor, Context
from helper_functions.home_devices_manipulations import dimmable_lights_manipulations
from helper_functions.translator import translate

logger = logging.getLogger(__name__)

# re patterns for the functions below
weather_pattern = re.compile(r'(what|\btell\b).*\bweather\b', re.I)
greeting_pattern = re.compile(r'\bhi|hello|hey\b', re.I)
appreciate_pattern = re.compile(r'thank|\bgood\b|\bnice\b|\bokay\b', re.I)
light_pattern = re.compile(r'(turn\s)(off|on)(.*light+)', re.I)
dimming_pattern = re.compile(r'(dim)(.*light+)', re.I)
setting_temp_pattern = re.compile(r'(\bset\b).*(\btemperature\b).*(\bto\b)', re.I)
heating_pattern = re.compile(r'(\bheat\b)', re.I)
cooling_pattern = re.compile(r'(\bcool\b)', re.I)


def lang_condition(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    return ctx.misc.get('lang_change') == True


def greeting_condition(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    request = translate(ctx.misc.get('lang'), ctx.last_request)
    return bool(greeting_pattern.search(request))


def weather_condition(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    request = translate(ctx.misc.get('lang'), ctx.last_request)
    return bool(weather_pattern.search(request))


def condition_yes(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    return ctx.misc.get('binary_intent') == "yes"


def condition_no(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    return ctx.misc.get('binary_intent') == "no"


def appreciate_condition(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    request = translate(ctx.misc.get('lang'), ctx.last_request)
    return bool(appreciate_pattern.search(request))


def room_condition(ctx: Context, actor: Actor) -> bool:
    return bool(ctx.misc.get('room'))


def light_condition(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    request = translate(ctx.misc.get('lang'), ctx.last_request)
    return bool(light_pattern.search(request))


def dim_condition(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    request = translate(ctx.misc.get('lang'), ctx.last_request)
    return bool(dimming_pattern.search(request))


def check_dimmable(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    if ctx.misc.get('room') is None:
        return False
    return dimmable_lights_manipulations(todo=0, room=ctx.misc.get('room'), check=True)


def get_brightness(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    return bool(ctx.misc.get('percentage'))


def setting_temp_condition(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    request = translate(ctx.misc.get('lang'), ctx.last_request)
    return bool(setting_temp_pattern.search(request))


def heating_condition(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    request = translate(ctx.misc.get('lang'), ctx.last_request)
    return bool(heating_pattern.search(request))


def cooling_condition(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    request = translate(ctx.misc.get('lang'), ctx.last_request)
    return bool(cooling_pattern.search(request))

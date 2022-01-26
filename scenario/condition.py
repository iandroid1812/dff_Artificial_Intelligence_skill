import logging
import re
from df_engine.core import Actor, Context

logger = logging.getLogger(__name__)

# re patterns for the functions below
weather_pattern = re.compile(r'(what|\btell\b).*\bweather\b', re.I)
greeting_pattern = re.compile(r'\bhi|hello|hey\b', re.I)
goodbye_pattern = re.compile(r'\bbye|goodbye|see\syou\b', re.I)
appreciate_pattern = re.compile(r'thank|\bgood\b|\bnice\b|\bokay\b|\bok\b', re.I)
light_pattern = re.compile(r'(turn\s)(off|on)(.*light+)', re.I)
dimming_pattern = re.compile(r'(dim)(.*light+)', re.I)
setting_temp_pattern = re.compile(r'(\bset\b).*(\btemperature\b).*(\bto\b).*(degree)', re.I)
heating_pattern = re.compile(r'(\bheat\b|\bwarm\b)', re.I)
cooling_pattern = re.compile(r'(\bcool\b)', re.I)
tts_pattern = re.compile(r'(\bturn off|disable|turn on|enable\b).*(\btts\b)', re.I)
q_a_pattern = re.compile(r'(\bwant\b).*(question)', re.I)


def lang_condition(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    return ctx.misc.get('lang_change') is True


def greeting_condition(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    request = '' if ctx.misc.get('translated') is None else ctx.misc.get('translated')
    return bool(greeting_pattern.search(request))


def beginning_condition(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    if len(ctx.labels) == 0:
        return True
    elif list(ctx.labels.values())[-1] == ('service_flow', 'start_node'):
        return True
    return False


def goodbye_condition(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    request = '' if ctx.misc.get('translated') is None else ctx.misc.get('translated')
    return bool(goodbye_pattern.search(request))


def weather_condition(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    request = '' if ctx.misc.get('translated') is None else ctx.misc.get('translated')
    return bool(weather_pattern.search(request))


def condition_yes(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    return ctx.misc.get('binary_intent') == "yes"


def condition_no(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    return ctx.misc.get('binary_intent') == "no"


def appreciate_condition(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    request = '' if ctx.misc.get('translated') is None else ctx.misc.get('translated')
    return bool(appreciate_pattern.search(request))


def room_condition(ctx: Context, actor: Actor) -> bool:
    return bool(ctx.misc.get('room'))


def light_condition(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    request = '' if ctx.misc.get('translated') is None else ctx.misc.get('translated')
    return bool(light_pattern.search(request))


def dim_condition(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    request = '' if ctx.misc.get('translated') is None else ctx.misc.get('translated')
    return bool(dimming_pattern.search(request))


def dimmable_condition(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    return bool(ctx.misc.get('dimmable'))


def get_brightness(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    return bool(ctx.misc.get('percentage'))


def setting_temp_condition(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    request = '' if ctx.misc.get('translated') is None else ctx.misc.get('translated')
    return bool(setting_temp_pattern.search(request))


def heating_condition(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    request = '' if ctx.misc.get('translated') is None else ctx.misc.get('translated')
    return bool(heating_pattern.search(request))


def cooling_condition(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    request = '' if ctx.misc.get('translated') is None else ctx.misc.get('translated')
    return bool(cooling_pattern.search(request))


def away(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    return ctx.misc.get('presence') == 'away'


def coming(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    return ctx.misc.get('presence') == 'coming'


def tts_check(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    request = '' if ctx.misc.get('translated') is None else ctx.misc.get('translated')
    return bool(tts_pattern.search(request))


def question_answer(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    request = '' if ctx.misc.get('translated') is None else ctx.misc.get('translated')
    return bool(q_a_pattern.search(request))

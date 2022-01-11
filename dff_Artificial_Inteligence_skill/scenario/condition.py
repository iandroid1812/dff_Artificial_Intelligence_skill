# for conditions
# TODO: add conditions

import logging
import re

from df_engine.core import Actor, Context

logger = logging.getLogger(__name__)

# re patterns for the functions below
weather_pattern = re.compile(r'(what|\btell\b).*\bweather\b', re.I)
greeting_pattern = re.compile(r'\bhi|hello|hey\b', re.I)
appreciate_pattern = re.compile(r'thank|\bgood\b|\bnice\b', re.I)
light_pattern = re.compile(r'(turn\s)(off|on)(.*light+)', re.I)
room_pattern = re.compile(r'\bhall\b|\bliving room\b|\bkitchen\b|\bbedroom\b', re.I)


def greeting_condition(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    return bool(greeting_pattern.search(ctx.last_request))


def weather_condition(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    return bool(weather_pattern.search(ctx.last_request))


def condition_yes(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    return bool(ctx.misc.get("confirm_intent"))


# added a yes/no
def condition_no(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    return bool(ctx.misc.get("deny_intent"))


def appreciate_condition(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    return bool(appreciate_pattern.search(ctx.last_request))


def light_condition(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    return bool(light_pattern.search(ctx.last_request))


def room_condition(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    return bool(room_pattern.search(ctx.last_request))


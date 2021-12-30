# for conditions
# TODO: add conditions

import logging
import re

from df_engine.core import Actor, Context

logger = logging.getLogger(__name__)

weather_pattern = re.compile(r'(what|\btell\b).*\bweather\b', re.IGNORECASE)
greeting_pattern = re.compile(r'\bhi|hello|hey\b', re.IGNORECASE)
appreciate_pattern = re.compile(r'thank|\bgood\b|\bnice\b', re.IGNORECASE)


def greeting_condition(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    request = ctx.last_request
    return bool(greeting_pattern.search(request))


def weather_condition(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    request = ctx.last_request
    return bool(weather_pattern.search(request))


def extra_weather_condition(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    return bool(ctx.misc.get("confirm_intent"))


def appreciate_condition(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    request = ctx.last_request
    return bool(appreciate_pattern.search(request))

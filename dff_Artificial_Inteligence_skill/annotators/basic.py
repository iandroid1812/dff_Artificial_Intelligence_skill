import re

from df_engine.core import Context


def binary_intent(ctx: Context):
    confirm_regexp = re.compile(r'\byes|yep|ok\b', re.IGNORECASE)
    deny_regexp = re.compile(r'\bno|nope\b', re.IGNORECASE)

    if confirm_regexp.search(ctx.last_request):
        ctx.misc['confirm_intent'] = bool(confirm_regexp.search(ctx.last_request))
    elif deny_regexp.search(ctx.last_request):
        ctx.misc['deny_intent'] = bool(deny_regexp.search(ctx.last_request))

    return ctx


def lights_intent(ctx: Context):
    if re.compile(r'\bon\b', re.I).search(ctx.last_request):
        ctx.misc['light_action'] = 'on'
    elif re.compile(r'\boff\b', re.I).search(ctx.last_request):
        ctx.misc['light_action'] = 'off'

    return ctx

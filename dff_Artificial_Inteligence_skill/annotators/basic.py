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

import re

from df_engine.core import Context


def language_intent(ctx: Context):
    ctx.misc['lang'] = 'ENG'
    russian_regexp = re.compile(r'\brussian|русский|rus|рус\b', re.I)
    if russian_regexp.search(ctx.last_request):
        ctx.misc['lang'] = 'RUS'
    return ctx


def binary_intent(ctx: Context):
    confirm_regexp = re.compile(r'\byes|yep|ok\b', re.I)
    deny_regexp = re.compile(r'\bno|nope\b', re.I)

    turn_on_regexp = re.compile(r'\bon\b', re.I)
    turn_off_regexp = re.compile(r'\boff\b', re.I)

    if confirm_regexp.search(ctx.last_request):
        ctx.misc['binary_intent'] = "yes"
    elif deny_regexp.search(ctx.last_request):
        ctx.misc['binary_intent'] = "no"
    else:
        ctx.misc['binary_intent'] = None

    if turn_on_regexp.search(ctx.last_request):
        ctx.misc['light_action'] = "on"
    elif turn_off_regexp.search(ctx.last_request):
        ctx.misc['light_action'] = "off"
    elif 'light_action' not in ctx.misc.keys():
        ctx.misc['light_action'] = None

    return ctx


def room_intent(ctx: Context):
    room_pattern = re.compile(r'\bhall\b|\bliving room\b|\bkitchen\b|\bbedroom\b', re.I)

    room = room_pattern.search(ctx.last_request)
    if room:
        ctx.misc['room'] = room[0]
    elif 'room' not in ctx.misc.keys():
        ctx.misc['room'] = None
    return ctx


def numerical_values(ctx: Context):
    percentage_pattern = re.compile(r'(\d+(\.\d+)?%)', re.I)
    temperature_pattern = re.compile(r'(\b\d{2}\b)(.*degree+)', re.I)

    percentage = percentage_pattern.search(ctx.last_request)
    ctx.misc['percentage'] = int(percentage[0][:-1]) if percentage else None

    temp = temperature_pattern.search(ctx.last_request)
    ctx.misc['temperature'] = int(temp[0].split()[0]) if temp else None
    return ctx

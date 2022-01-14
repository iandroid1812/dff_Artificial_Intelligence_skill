import re

from df_engine.core import Context
from helper_functions.translator import translate


def language_intent(ctx: Context):
    russian_regexp = re.compile(r'\brussian|русский|rus|рус\b', re.I)
    english_regexp = re.compile(r'\benglish|английский|eng|англ\b', re.I)

    ctx.misc['lang'] = 'ENG' if 'lang' not in ctx.misc.keys() else ctx.misc['lang']

    if russian_regexp.search(ctx.last_request):
        ctx.misc['lang'] = 'RUS'
        ctx.misc['lang_change'] = True
        return ctx
    elif english_regexp.search(ctx.last_request):
        ctx.misc['lang'] = 'ENG'
        ctx.misc['lang_change'] = True
        return ctx

    ctx.misc['lang_change'] = False
    return ctx


def binary_intent(ctx: Context):
    request = translate(ctx.misc.get('lang'), ctx.last_request)

    confirm_regexp = re.compile(r'\byes|yep|ok\b', re.I)
    deny_regexp = re.compile(r'\bno|nope\b', re.I)

    turn_on_regexp = re.compile(r'\bon\b', re.I)
    turn_off_regexp = re.compile(r'\boff\b', re.I)

    if confirm_regexp.search(request):
        ctx.misc['binary_intent'] = "yes"
    elif deny_regexp.search(request):
        ctx.misc['binary_intent'] = "no"
    else:
        ctx.misc['binary_intent'] = None

    if turn_on_regexp.search(request):
        ctx.misc['light_action'] = "on"
    elif turn_off_regexp.search(request):
        ctx.misc['light_action'] = "off"
    elif 'light_action' not in ctx.misc.keys():
        ctx.misc['light_action'] = None

    return ctx


def room_intent(ctx: Context):
    request = translate(ctx.misc.get('lang'), ctx.last_request)

    room_pattern = re.compile(r'\bhall\b|\bcorridor\b|\blobby\b|\bliving room\b|\bkitchen\b|\bbedroom\b', re.I)

    room = room_pattern.search(request)
    if room:
        ctx.misc['room'] = room[0] if room[0] not in {'corridor', 'lobby'} else 'hall'
    elif 'room' not in ctx.misc.keys():
        ctx.misc['room'] = None
    return ctx


def numerical_values(ctx: Context):
    request = translate(ctx.misc.get('lang'), ctx.last_request)

    percentage_pattern = re.compile(r'(\d+(\.\d+)?%)', re.I)
    temperature_pattern = re.compile(r'(\b\d{2}\b)(.*degree+)', re.I)

    percentage = percentage_pattern.search(request)
    ctx.misc['percentage'] = int(percentage[0][:-1]) if percentage else None

    temp = temperature_pattern.search(request)
    ctx.misc['temperature'] = int(temp[0].split()[0]) if temp else None
    return ctx

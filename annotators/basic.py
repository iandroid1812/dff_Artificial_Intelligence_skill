import re
from df_engine.core import Context
from helper_functions.translator_tts import translate
from helper_functions.home_devices_manipulations import check_dimmable


def ctx_reset(ctx: Context, log=False):
    if len(ctx.labels) >= 2 and list(ctx.labels.values())[-1] == ('service_flow', 'start_node'):
        # we need to clear misc dict from previous context, because after we reach the start node
        # our previous conversation was already finished/stopped, and it's context is irrelevant
        # except the language that we were using and the TTS status
        ctx.misc = {'lang': ctx.misc['lang'],
                    'lang_change': ctx.misc['lang_change'],
                    'tts': ctx.misc['tts']}
    if log and not ctx.validation:
        print("Labels:", ctx.labels)
        print("Misc", ctx.misc)
    return ctx


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


def translate_request(ctx: Context):
    ctx.misc['translated'] = translate(ctx.misc.get('lang'), ctx.last_request)
    return ctx


def tts_status(ctx: Context):
    tts_pattern_off = re.compile(r'(\bturn off|disable\b).*(\btts\b)', re.I)
    tts_pattern_on = re.compile(r'(\bturn on|enable\b).*(\btts\b)', re.I)

    if len(ctx.labels) >= 1 and list(ctx.labels.values())[-1] == ('service_flow', 'Q&A'):
        return ctx

    request = ctx.misc['translated']
    ctx.misc['tts'] = ctx.misc['tts'] if 'tts' in ctx.misc else True
    if tts_pattern_off.search(request):
        ctx.misc['tts'] = False
    elif tts_pattern_on.search(request):
        ctx.misc['tts'] = True
    return ctx


def binary_intent(ctx: Context):
    confirm_regexp = re.compile(r'\byes|yep|ok\b', re.I)
    deny_regexp = re.compile(r'\bno|nope\b', re.I)
    turn_on_regexp = re.compile(r'\bturn\b\s\bon\b', re.I)
    turn_off_regexp = re.compile(r'\bturn\b\s\boff\b', re.I)

    request = ctx.misc['translated']

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
    room_pattern = re.compile(r'hall|\bcorridor\b|\blobby\b|\bliving room\b|\bkitchen\b|\bbedroom\b', re.I)

    request = ctx.misc['translated']
    room = room_pattern.search(request)

    if room:
        # added corridor and lobby because of similar definitions to 'hall'
        ctx.misc['room'] = room[0] if room[0] not in {'corridor', 'lobby'} else 'hall'
    elif 'room' not in ctx.misc.keys():
        ctx.misc['room'] = None
    ctx.misc['dimmable'] = check_dimmable(ctx.misc.get('room'))
    return ctx


def numerical_values(ctx: Context):
    percentage_pattern = re.compile(r'(\d+(\.\d+)?%)', re.I)
    temperature_pattern = re.compile(r'(\b\d{2}\b)(.*degree+)', re.I)

    request = ctx.misc['translated']
    percentage = percentage_pattern.search(request)
    temp = temperature_pattern.search(request)

    ctx.misc['percentage'] = int(percentage[0][:-1]) if percentage else ctx.misc.get('percentage')
    ctx.misc['temperature'] = int(temp[0].split()[0]) if temp else ctx.misc.get('temperature')
    return ctx


def home_presence(ctx: Context):
    away_pattern = re.compile(r'((go).*(\baway\b))|(\bleave\b|\bleaving\b)', re.I)
    coming_pattern = re.compile(r'(\bcoming\b|\bgoing\b|\breturning\b).*(home)', re.I)

    request = ctx.misc['translated']
    away = away_pattern.search(request)
    coming = coming_pattern.search(request)
    if 'presence' not in set(ctx.misc.keys()):
        ctx.misc['presence'] = None
    ctx.misc['presence'] = 'coming' if coming else ctx.misc['presence']
    ctx.misc['presence'] = 'away' if away else ctx.misc['presence']
    return ctx

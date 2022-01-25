import re

features = re.compile(r'(what).*(do|capabilities)', re.I)
lang = re.compile(r'(change).*(language)', re.I)
temperature = re.compile(r'(temperature)', re.I)
heating = re.compile(r'(heat)', re.I)
cooling = re.compile(r'(cool)', re.I)
lights = re.compile(r'(lamp|light)', re.I)
dim = re.compile(r'(dim)', re.I)


def q_a_bot(request):
    if features.search(request):
        answer = "I can control the temperature and light groups in your home, tell you a weather forecast." \
                 "\nYou can tell me if you are leaving or coming home to launch certain scenarios."
    elif lang.search(request):
        answer = "To change the language, just type in the required language (russian/english)."
    elif temperature.search(request):
        answer = "To choose certain temperature, say \"set temperature to 28 degrees in the hall\"."
    elif heating.search(request):
        answer = "You need to just say \"Heat up the kitchen\""
    elif cooling.search(request):
        answer = "You need to just say \"Cool down the room\""
    elif dim.search(request):
        answer = "You can say \"Dim the light\", \"Dim the lights in the bedroom\"."
    elif lights.search(request):
        answer = "To control the lights, just say \"Turn off/on the lights\", you can specify the room as well."
    else:
        answer = "I do not know the answer to this question, sorry.\n" \
                 "Remember that you can stop conversation at any time by saying \"stop\"."
    return answer

from helper_functions.requesting import weather_forecast_request

data = weather_forecast_request()
degree = u'\N{DEGREE SIGN}'

testing_dialog = [
    # First we must disable tts for dialogues testing
    ("TURN OFF TTS",
     "The TTS functionality was disabled successfully!"),

    # start of convo 1
    ("Hi",
     "Hi, I am your Home Assistant. How can I help?"),

    ("Please, tell me about the weather.",
     f"The temperature in {data['loc']} is {data['temp']}{degree}C. It feels like {data['feels-like']}{degree}C." \
     "\nDo you want to get more information?"),

    ("Ok",
     f"Weather report: {data['report']}. The humidity level is {data['humidity']}% " \
     f"and the wind speed is {data['wind']} m/s."),

    ("Great, thank you!",
     "Glad I could help!"),

    # start of convo 2
    ("Whats the weather outside?",
     f"The temperature in {data['loc']} is {data['temp']}{degree}C. It feels like {data['feels-like']}{degree}C." \
     "\nDo you want to get more information?"),

    ("Nope",
     "Ok, that's it for the weather then. Anything else?"),

    ("No",
     "I'm waiting for the command..."),

    # start of convo 3
    ("HEY",
     "Hi, I am your Home Assistant. How can I help?"),

    ("Turn on the lights please.",
     "Ok, in which room?"),

    ("In the garage",
     "Ok, in which room?"),

    ("The bedroom",
     "Turned on the lights in the bedroom.\nDo you want to dim the light as well?"),

    ("ok",
     "What brightness do you want?"),

    ("Let's dim to 25%",
     "Dimmed the light in the bedroom to 25%"),

    ("Good job",
     "Glad I could help!"),

    # start of convo 4
    ("Please set the temperature to 29 degreed in the hall.",
     "The temperature in the hall was set to 29 degrees"),

    ("good job",
     "Glad I could help!"),

    # start of convo 5
    ("Turn off the lights in the kitchen",
     "Turned off the lights in the kitchen.\nIs that all?"),

    ("yes, thank you",
     "Glad I could help!"),


    # start of convo 6
    ("Русский язык",
     "Изменение языка успешно"),

    ("Включи свет, пожалуйста",
     "Хорошо, в какой комнате?"),

    ("В подвале",
     "Хорошо, в какой комнате?"),

    ("В гостинной",
     "Включил свет в гостиной.\nЭто все?"),

    ("Да",
     "жду команды..."),

    ("Поставь температуру в спальне на 25 градусов",
     "Температура в спальне была установлена на 25 градусов."),

    # start of convo 7
    ("Здравствуй",
     "Привет, я твой домашний помощник. Чем я могу помочь?"),

    ("Выключи свет",
     "Хорошо, в какой комнате?"),

    ("стоп",
     "Разговор остановлен. Чтобы начать, скажите: «начать»."),

    ("Привет",
     "Разговор остановлен. Чтобы начать, скажите: «начать»."),

    ("Начать",
     "жду команды..."),

    # start of convo 8
    ("Я хочу задать вопрос",
     "Хорошо, спроси меня."),

    ("Как мне приглушить свет в комнате?",
     "Вы можете сказать «Приглушите свет», «Приглушите свет в спальне»."),

    ("Как менять температуру?",
     "Чтобы выбрать определенную температуру, скажите «установите температуру 28 градусов в прихожей»."),

    ("Как подогреть помещение?",
     "Вам нужно просто сказать: «Разогрейте кухню»."),

    ("2861Привет",
     "Я не знаю ответа на этот вопрос, извините.\nПомните, что вы можете остановить разговор "
     "в любой момент, сказав «стоп»."),

    ("Стоп",
     "Разговор остановлен. Чтобы начать, скажите: «начать»."),

    ("Начать",
     "жду команды..."),

    # start of convo 9
    ("Включи английский язык",
     "Language change successful"),

    ("I want to ask some questions.",
     "Ok, ask me."),

    ("How to turn on the lamps?",
     "To control the lights, just say \"Turn off/on the lights\", you can specify the room as well."),

    ("It is too hot, I need to cool down",
     "You need to just say \"Cool down the room\""),

    ("stop",
     "The conversation has been stopped. In order to begin say: 'start'.")
]


def preparation():
    return testing_dialog

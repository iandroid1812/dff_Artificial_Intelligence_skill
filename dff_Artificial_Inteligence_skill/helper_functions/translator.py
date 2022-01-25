from deep_translator import GoogleTranslator as Translator
from typing import Optional
from gtts import gTTS
import pyglet
# pyglet is much better than playsound in this situation, because we can play
# the sound and continue execution of the other commands while the tts is playing
# instead of waiting for an audio stream to end.


def translate(lang: str, string: str, option: Optional[str] = None, log=False) -> str:
    if string == '':
        return ''

    if lang == 'RUS':
        if option == 'response':
            translator = Translator(target='ru')
        else:
            translator = Translator(target='en')
        translation = translator.translate(string)
        if log:
            print("FROM:", string, "\n" "TO", translation)
        # sometimes translator gave string with 'zero width white space', that is why
        # here it is replaced with an empty string instead to fix this error
        return translation.replace('\u200b', '')
    return string


def text_to_speech(response: str, lang: str, validation: bool, tts: bool):
    if validation or not tts:
        return

    if lang == 'RUS':
        tts = gTTS(response, lang='ru', slow=False)
    else:
        tts = gTTS(response, lang='en', slow=False)

    tts.save("./helper_functions/voice_container/voice.wav")
    pyglet.resource.path = ['./helper_functions/voice_container']
    sound = pyglet.resource.media("voice.wav", streaming=False)
    sound.play()

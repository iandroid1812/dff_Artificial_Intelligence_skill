from deep_translator import GoogleTranslator as Translator
from typing import Optional
from gtts import gTTS
import pyglet
# pyglet is much better than playsound in this situation, because we can play
# the sound and continue execution of the other commands while the tts is playing
# instead of waiting for an audio stream to end like in playsound


# make log=True to see translation process in order to examine multilingual incompatibilities
def translate(lang: str, string: str, option: Optional[str] = None, log=False) -> str:
    if string == '':
        return ''

    if lang == 'RUS':
        if option == 'response':
            translator = Translator(target='ru')
        else:
            translator = Translator(target='en')
        # fix for an edge case of incorrect translation
        translation = translator.translate(string).replace('зале', 'прихожей')
        if log:
            print("FROM:", string, "\n" "TO", translation)
        # sometimes translator gave string with 'zero width white space', that is why
        # here it is replaced with an empty string instead to fix this error
        return translation.replace('\u200b', '')
    return string


def text_to_speech(response: str, lang: str, validation: bool, tts: bool):
    # we don't need tts during validation loop and if tts is disabled by user
    if validation or not tts:
        return

    if lang == 'RUS':
        tts = gTTS(response, lang='ru', slow=False)
    else:
        tts = gTTS(response, lang='en', slow=False)

    # saving .wav file to a voice_container, so we can play it from there
    # the file rewrites itself each time tts is used, so it does not take too much space
    tts.save("./helper_functions/voice_container/voice.wav")
    pyglet.resource.path = ['./helper_functions/voice_container']
    sound = pyglet.resource.media("voice.wav", streaming=False)
    sound.play()

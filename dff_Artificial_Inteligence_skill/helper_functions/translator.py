from deep_translator import GoogleTranslator as Translator


def translate(lang: str, string: str, option=None, log=False) -> str:
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
        return translation
    return string

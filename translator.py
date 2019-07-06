import codecs
import json
import os
import shutil
import sys

import click
from googletrans import Translator

from lang_codes import *


@click.command()
@click.option('--in-lang', default='en', help='Language you are translating from.')
@click.option('--out-lang', default='en,es', help='CSV of languages you are going to')
@click.option('--file', default='messages.json', help='Path to your messages.json file you want translated')
@click.option('--remove-locale', default=True, help='Should remove the existing locales folder')
def translate(in_lang, out_lang, file, remove_locale):
    translator = Translator()
    messages = json.loads(open(file).read())
    langs = out_lang.split(',')
    translations = {}

    # Generate dictionary of all languages requested
    for lang in langs:
        if lang not in chrome_langs:
            sys.exit('Selected output language not accepted by Chrome!')
        if lang not in google_translate_langs:
            sys.exit('Selected language cannot be translated by Google Chrome!')
        translations[lang] = {}

    for key in messages.keys():
        for lang in langs:
            # if we're translating to the same language, skip it
            if lang == in_lang:
                continue
            actual_string = messages[key]['message']
            trans_string = translator.translate(actual_string, src=in_lang, dest=lang)
            translations[lang][key] = {'message': trans_string.text}
    write_translations(translations, remove_locale)


def write_translations(translations, remove_locale):
    # delete locales if it already exists
    if remove_locale and os.path.isdir('_locales'):
        shutil.rmtree('_locales')
    os.mkdir('_locales')
    for lang in translations.keys():
        if not os.path.isdir('_locales/' + lang):
            os.mkdir('_locales/' + lang)
        with codecs.open('_locales/' + lang + '/messages.json', 'w', encoding='utf-8') as outfile:
            json.dump(translations[lang], outfile, ensure_ascii=False)


if __name__ == '__main__':
    translate()

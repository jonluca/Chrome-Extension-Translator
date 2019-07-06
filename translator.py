import codecs
import json
import os
import shutil
import sys

import chalk
import click
from googletrans import Translator

from lang_codes import *

chrome_langs_csv = ','.join(chrome_langs)


@click.command()
@click.option('--in-lang', default='en', help='Language you are translating from.')
@click.option('--out-lang', default=chrome_langs_csv,
              help='CSV of languages you\'d like to translate to, default to all langues:\n' + chrome_langs_csv)
@click.option('--file', default='messages.json', help='Path to your messages.json file you want translated')
@click.option('--remove-locale', default=True, type=bool, help='Should remove the existing locales folder')
def translate(in_lang, out_lang, file, remove_locale):
    translator = Translator()
    messages = json.loads(open(file).read())
    langs = out_lang.split(',')
    translations = {}

    # Generate dictionary of all languages requested
    for lang in langs:
        lang_map = mapping_chrome_langs_to_google_translate[lang]
        if lang not in chrome_langs:
            sys.exit(f'Selected output language {lang} not accepted by Chrome!')
        if lang_map not in google_translate_langs:
            sys.exit(f'Selected language {lang} cannot be translated by Google Chrome!')
        translations[lang] = {}

    for lang in langs:
        try:
            # if we're translating to the same language, save it and then skip it
            if lang == in_lang:
                translations[lang] = messages
                continue
            click.echo(f'Translating {lang}')
            for key in messages.keys():
                actual_string = messages[key]['message']
                # the short codes between GTrans and GChrome are different, so dest should be the mapping we know
                lang_map = mapping_chrome_langs_to_google_translate[lang]
                trans_string = translator.translate(actual_string, src=in_lang, dest=lang_map)
                translations[lang][key] = {'message': trans_string.text}
            write_translations(translations, remove_locale)
        except Exception as e:
            click.echo(chalk.red(f'Error translating language: {lang} - skipping'))
            click.echo(e)
    click.echo("""
    Done!
    
    Note: The saved _locales folder might not have the correct folder names. Verify and rename the appropriately according to this site:
    
    https://developer.chrome.com/webstore/i18n?csw=1#localeTable
    
    That the locale is named with the appropriate short code. 
    
    This is due to slight differences between the translation short codes used by google translate and google chrome.
    """)


def write_translations(translations, remove_locale):
    # delete locales if it already exists
    if remove_locale and os.path.isdir('_locales'):
        shutil.rmtree('_locales')
    os.mkdir('_locales')
    for lang in translations.keys():
        if not os.path.isdir('_locales/' + lang):
            os.mkdir('_locales/' + lang)
        try:
            with codecs.open('_locales/' + lang + '/messages.json', 'w', encoding='utf-8') as outfile:
                json.dump(translations[lang], outfile, ensure_ascii=False)
        except Exception as e:
            print(chalk.red(f'Error writing {lang}: {e}'))


if __name__ == '__main__':
    translate()

# Chrome Extension Translator

Given a top level `messages.json`, this extension will attempt to create a `_locales` folder with the requested languages.

## Usage

```text
Usage: translator.py [OPTIONS]

Options:
  --in-lang TEXT           Language you are translating from.
  --out-lang TEXT          CSV of languages you'd like to translate to,
                           default to all langues:
                           ar,am,bg,bn,ca,cs,da,de,el,
                           en,en_GB,en_US,es,es_419,et,fa,fi,fil,fr,gu,he,hi,h
                           r,hu,id,it,ja,kn,ko,lt,lv,ml,mr,ms,nl,no,pl,pt_BR,p
                           t_PT,ro,ru,sk,sl,sr,sv,sw,ta,te,th,tr,uk,vi,zh_CN,z
                           h_TW
  --file TEXT              Path to your messages.json file you want translated
  --remove-locale BOOLEAN  Should remove the existing locales folder
  --help                   Show this message and exit.
```

## Sample

```bash
python translator.py --in-lang=en --out-lang=en,es,it,zh_CN,fr --remove-locale=false
```

## Important Notes

If you start getting "Error translating language: LANG - skipping", it most likely means that you are being rate limited by Google.

Either switch to a VPN/set up some rotating proxies or wait it out. 
# -*- coding: utf-8 -*-
'''
setlabeldesc.py

Script to set labels and descriptions in Wikidata items

The script run a SPARQL query in the Wikidata Query Service (WDQS) and then
check if each item has or not a label or description in the language chosen
by the operator of the script.

It is a derivative work of the Edoderoobot's script labels-indonesian-item.py,
made by Edoderoo for Wikidata. You can check the original sourcecode here:
    https://www.wikidata.org/wiki/User:Edoderoobot/labels-indonesian-item.py

Distributed under the terms of the GNU General Public License v3.0
'''

import colorama as c
import datetime

# Pywikibot
from pywikibot import pagegenerators as pg
import pywikibot

# Local modules
import log

# Configuration
site = pywikibot.Site("wikidata", "wikidata")
scriptName = "setlabeldesc"
now = datetime.datetime.now()
timestamp = str(now.strftime("%Y-%m-%d %H:%M"))

# Colorama reset
cR = c.Style.RESET_ALL


def sparqlQuery(query):
    '''
    Pending to value the possible migration to utils.py
    '''

    wdSite = pywikibot.Site("wikidata", "wikidata")
    generator = pg.WikidataSPARQLPageGenerator(query, site=wdSite)

    for wd in generator:
        if (wd.exists()):
            wd.get(get_redirect=True)
            yield wd


def setLabel(query, desc, lang, sourceLang, edit=False):
    # Check if the script is running a test or is making editions
    if edit is True:
        script = scriptName + "-" + sourceLang + "-" + lang
        print("\nModo de edición")
    else:
        script = scriptName + "-test-" + sourceLang + "-" + lang
        print("\nModo de pruebas")

    langBlank = 0
    langFilled = 0

    for item in sparqlQuery(query):
        if sourceLang in item.labels:
            sourceLang = item.labels[sourceLang]
            if lang in item.labels:
                lang = item.labels[lang]
                langFilled += 1
                existed = f"¡Ya existe la etiqueta en {lang}! Revisar descripción: {item.title()}-{100 * langFilled / (langBlank + langFilled + 1)}-{langFilled}-{langBlank}-{lang}]-<{sourceLang}>"
                # existed = u"¡Ya existe la etiqueta en {}! Revisar descripción: {}-{}-{}-{}-[{}]-<{}>".format(lang, item.title(), 100 * langFilled / (langBlank + langFilled + 1), langFilled, langBlank, lang, sourceLang)

                log.check(existed, script)
            else:
                langBlank += 1

                data = {}
                data.update({"labels": {lang: sourceLang}})
                data.update({"descriptions": {lang: desc}})

                print("[{}]-<{}>".format(lang, sourceLang))

                if edit is True:
                    try:
                        item.editEntity(data, summary=f"set {lang}-label and {lang}-desc from {sourceLang}-wiki")
                        print(f"Se ha editado el elemento.\n{data}")
                        log.check(data, script)
                    except Exception as e:
                        print(e)
                        log.check(e, script)
                        pass
                if edit is False:
                    try:
                        print(f"No se ha editado el elemento (modo de pruebas).\n{data}")
                        log.check(data, script)
                    except Exception as e:
                        print(e)
                        log.check(e, script)
                        pass
                else:
                    print("Algo no ha funcionado correctamente")

        else:
            notExisted = f"¡No existe la etiqueta en {sourceLang}! {item.title()}-{100 * langFilled / (langBlank + langFilled + 1)}-{langFilled}-{langBlank}-[{lang}]-<{sourceLang}>"
            print(notExisted)

            log.check(notExisted, script)

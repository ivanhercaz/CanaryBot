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

# Pywikibot
from pywikibot import pagegenerators as pg
import pywikibot

# Local modules
import log

# Global variables
scriptName = "setlabeldesc"

def sparqlQuery(query):
  wdSite = pywikibot.Site("wikidata", "wikidata")
  generator = pg.WikidataSPARQLPageGenerator(query, site = wdSite)

  for wd in generator:
    if (wd.exists()):
      wd.get(get_redirect = True)
      yield wd

def setLabel(query, desc, lang, sourceLang, edit = False):
    # Check if the script is running a test or is making editions
    if edit == True:
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
                existed = u"¡Ya existe la etiqueta en {}! Revisar descripción: {}-{}-{}-{}-[{}]-<{}>".format(lang, item.title(), 100 * langFilled / (langBlank + langFilled + 1), langFilled, langBlank, lang, sourceLang)

                log.check(existed, script)
            else:
                langBlank += 1

                data = {}
                data.update({"labels": {lang: sourceLang} })
                data.update({"descriptions": {lang: desc} })

                print("[{}]-<{}>".format(lang, sourceLang))

                if edit == True:
                    try:
                        item.editEntity(data, summary = u"set {0}-label and {0}-desc from {1}-wiki".format(lang, sourceLang))
                        print("Se ha editado el elemento.\n" + data)
                        log.check(data, script)
                    except Exception as e:
                        print(e)
                        log.check(e, script)
                        pass
                if edit == False:
                    try:
                        print("No se ha editado el elemento (modo de pruebas).\n" + data)
                        log.check(data, script)
                    except Exception as e:
                        print(e)
                        log.check(e, script)
                        pass
                else:
                    print("Algo no ha funcionado correctamente")

        else:
            notExisted = u"¡No existe la etiqueta en {}! {}-{}-{}-{}-[{}]-<{}>".format(sourceLang, item.title(), 100 * langFilled / (langBlank + langFilled + 1), langFilled, langBlank, lang, sourceLang)
            print(notExisted)

            log.check(notExisted, script)

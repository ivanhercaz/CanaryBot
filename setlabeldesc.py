# -*- coding: utf-8 -*-
# This script is a derivative work of the Edoderoobot's script labels-indonesian-villages.py
# made by Edoderoo for Wikidata. You can check the source code here:
# https://www.wikidata.org/wiki/User:Edoderoobot/labels-indonesian-villages.py
# Now I am working on this script to make more powerful and useful for different cases

import logging, log
import pywikibot
from pywikibot import pagegenerators as pg

# Global variables
scriptName = "setlabeldesc"

def sparqlQuery(query):
  wdSite = pywikibot.Site("wikidata", "wikidata")
  generator = pg.WikidataSPARQLPageGenerator(query, site = wdSite)

  for wd in generator:
    if (wd.exists()):
      wd.get(get_redirect = True)
      yield wd

def setLabel(query, lang, sourceLang, edit = False):
    # Check if the script is running a test or is making editions
    if edit == True:
        script = scriptName + "-" + sourceLang + "-" + lang
        print("Modo de edición")
    else:
        script = scriptName + "-test-" + sourceLang + "-" + lang
        print("Modo de pruebas")

    langBlank = 0
    langFilled = 0

    for village in sparqlQuery(query):
        if sourceLang in village.labels:
            sourceLang = village.labels[sourceLang]
            if lang in village.labels:
                lang = village.labels[lang]
                langFilled += 1
                existed = u"¡Ya existe la etiqueta en {}! Revisar descripción: {}-{}-{}-{}-[{}]-<{}>".format(lang, village.title(), 100 * langFilled / (langBlank + langFilled + 1), langFilled, langBlank, lang, sourceLang)

                log.check(existed, script)
            else:
                langBlank += 1

                data = {}
                data.update({"labels": {lang: sourceLang} })
                data.update({"descriptions": {lang: "pueblo de Indonesia"}})

                print("[%s]-<%s>" % (lang, sourceLang))

                if edit == True:
                    try:
                        village.editEntity(data, summary = u"set {}-label and {}-desc from {}-wiki".format(lang, sourceLang))
                        print("Se ha editado el elemento.\n" + data)
                        log.check(data, script)
                    except:
                        pass
                if edit == False:
                    try:
                        print("No se ha editado el elemento (modo de pruebas).\n" + data)
                        log.check(data, script)
                    except:
                        pass
                else:
                    print("Algo no ha funcionado correctamente")

        else:
            notExisted = u"¡No existe la etiqueta en {}! {}-{}-{}-{}-[{}]-<{}>".format(sourceLang, village.title(), 100 * langFilled / (langBlank + langFilled + 1), langFilled, langBlank, lang, sourceLang)
            print(notExisted)

            log.check(notExisted, script)

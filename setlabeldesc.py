# -*- coding: utf-8 -*-
# This script is a derivative work of the Edoderoobot's script labels-indonesian-villages.py
# made by Edoderoo for Wikidata. You can check the source code here:
# https://www.wikidata.org/wiki/User:Edoderoobot/labels-indonesian-villages.py
# Now I am working on this script to make more powerful and useful for different cases

import logging, log
import pywikibot
from pywikibot import pagegenerators as pg

# Globa variables
scriptName = "setlabeldesc"

def sparqlQuery(query):
  wdSite = pywikibot.Site("wikidata", "wikidata")
  generator = pg.WikidataSPARQLPageGenerator(query, site = wdSite)

  for wd in generator:
    if (wd.exists()):
      wd.get(get_redirect = True)
      yield wd

def setLabel(query, lang, sourceLang):
    script = scriptName + "-" + sourceLang + "-" + lang

    langBlank = 0
    langFilled = 0

    for village in sparqlQuery(query):
        if sourceLang in village.labels:
            sourceLang = village.labels[sourceLang]
            if lang in village.labels:
                lang = village.labels[lang]
                langFilled += 1
                existed = u"¡Ya existe la etiqueta en español! Revisar descripción: %s-%d-%d-%d-[%s]-<%s>" % (village.title(), 100 * langFilled / (langBlank + langFilled + 1), langFilled, langBlank, lang, sourceLang)

                log.check(existed, script)
            else:
                langBlank += 1

                data = {}
                data.update({"labels": {lang: sourceLang} })
                data.update({"descriptions": {lang: "pueblo de Indonesia"}})

                print("[%s]-<%s>" % (lang, sourceLang))
                try:
                    # The next line is commented to test the script without making changes in Wikidata
                    #village.editEntity(data, summary = u"set lang-label and lang-desc from sourceLang-wiki")
                    print(data)

                    log.check(data, script)
                except:
                    pass
        else:
            notExisted = u"¡No existe la etiqueta en indonesio! %s-%d-%d-%d-[%s]-<%s>" % (village.title(), 100 * langFilled / (langBlank + langFilled + 1), langFilled, langBlank, lang, sourceLang)
            print(notExisted)

            log.check(notExisted, script)

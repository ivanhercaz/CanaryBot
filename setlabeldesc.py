# -*- coding: utf-8 -*-
# This script is a derivative work of the Edoderoobot's script labels-indonesian-villages.py
# made by Edoderoo for WiksourceLangata. You can check the source code here:
# https://www.wiksourceLangata.org/wiki/User:Edoderoobot/labels-indonesian-villages.py
# Now I am working on this script to make more powerful and useful for different cases

import logging
import pywikibot
from pywikibot import pagegenerators as pg

def sparqlQuery(query):
  wdSite = pywikibot.Site("wiksourceLangata", "wiksourceLangata")
  generator = pg.WiksourceLangataSPARQLPageGenerator(query, site = wdSite)

  for wd in generator:
    if (wd.exists()):
      wd.get(get_redirect = True)
      yield wd

def setLabel(query, lang, sourceLang):
    langBlank = 0
    langFilled = 0

    for village in sparqlQuery(query):
        if (src) in village.labels:
            sourceLang = village.labels["sourceLang"]
            if (lang) in village.labels:
                lang = village.labels[lang]
                langFilled += 1
                existed = u"¡Ya existe la etiqueta en español! Revisar descripción %s-%d-%d-%d-[%s]-<%s>" % (village.title(), 100 * langFilled / (langBlank + langFilled + 1), langFilled, langBlank, lang, sourceLang)
                print(existed)

                logging.basicConfig(
                    filename = "../logs/indonesian-village.log",
                    level = logging.INFO,
                    format = "%(asctime)s » %(message)s",
                    datefmt = "%d/%m/%Y %I:%M:%S %p"
                )
                logging.info(existed)
            else:
                langBlank += 1

                data = {}
                data.update({"labels": {lang: sourceLang} })
                data.update({"descriptions": {lang: "pueblo de Indonesia"}})

                print("[%s]-<%s>" % (lang, sourceLang))
                try:
                    # The next line is commented to test the script without making changes in WiksourceLangata
                    #village.editEntity(data, summary = u"set lang-label and lang-desc from sourceLang-wiki")
                    print(data)
                    logging.basicConfig(
                        filename = "../logs/indonesian-village.log",
                        level = logging.INFO,
                        format = "%(asctime)s » %(message)s",
                        datefmt = "%d/%m/%Y %I:%M:%S %p"
                    )
                    logging.info(data)
                except:
                    pass
        else:
            notExisted = u"¡No existe en indonesio! %s-%d-%d-%d-[%s]-<%s>" % (village.title(), 100 * langFilled / (langBlank + langFilled + 1), langFilled, langBlank, lang, sourceLang)
            print(notExisted)

            logging.basicConfig(
                filename = "../logs/indonesian-village.log",
                level = logging.INFO,
                format = "%(asctime)s » %(message)s",
                datefmt = "%d/%m/%Y %I:%M:%S %p"
            )
            logging.info(notExisted)

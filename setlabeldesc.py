# -*- coding: utf-8 -*-
# This script is a derivative work of the Edoderoobot's script labels-indonesian-villages.py
# made by Edoderoo for Wikidata. You can check the source code here:
# https://www.wikidata.org/wiki/User:Edoderoobot/labels-indonesian-villages.py
# Now I am working on this script to make more powerful and useful for different cases

import logging
import pywikibot
from pywikibot import pagegenerators as pg

query = "select ?item where {?item wdt:P31 wd:Q2225692 . ?item wdt:P17 wd:Q252}"
lang = "es"
src = "id"

def sparqlQuery(query):
  wdSite = pywikibot.Site("wikidata", "wikidata")
  generator = pg.WikidataSPARQLPageGenerator(query, site = wdSite)

  for wd in generator:
    if (wd.exists()):
      wd.get(get_redirect = True)
      yield wd


def setLabel(query):
    esBlank = 0
    esFilled = 0

    for village in sparqlQuery(query):
        es = ""
        id = ""
        if (src) in village.labels:
            id = village.labels["id"]
            if (lang) in village.labels:
                es = village.labels[lang]
                esFilled += 1
                existed = u"¡Ya existe la etiqueta en español! Revisar descripción %s-%d-%d-%d-[%s]-<%s>" % (village.title(), 100 * esFilled / (esBlank + esFilled + 1), esFilled, esBlank, es, id)
                print(existed)

                logging.basicConfig(
                    filename = "../logs/indonesian-village.log",
                    level = logging.INFO,
                    format = "%(asctime)s » %(message)s",
                    datefmt = "%d/%m/%Y %I:%M:%S %p"
                )
                logging.info(existed)
            else:
                esBlank += 1

                data = {}
                data.update({"labels": {lang: id} })
                data.update({"descriptions": {"es": "pueblo de Indonesia"}})

                print("[%s]-<%s>" % (es, id))
                try:
                    #village.editEntity(data, summary = u"set es-label and es-desc from id-wiki")
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
            notExisted = "¡No existe en indonesio! %s-%d-%d-%d-[%s]-<%s>" % (village.title(), 100 * esFilled / (esBlank + esFilled + 1), esFilled, esBlank, es, id)
            print(notExisted)

            logging.basicConfig(
                filename = "../logs/indonesian-village.log",
                level = logging.INFO,
                format = "%(asctime)s » %(message)s",
                datefmt = "%d/%m/%Y %I:%M:%S %p"
            )
            logging.info(notExisted)

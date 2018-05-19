# -*- coding: utf-8 -*-

import pywikibot, re, datetime, logging, readchar, sys
from pywikibot import pagegenerators as pg

site = pywikibot.Site("wikidata", "wikidata")


def editItem(item, replacement):
    print("Edit mode not ready!")
    print("Decision: ")

    key = repr(readchar.readkey())
    key = key.replace("'", "")

    while key is "e" or key is not "q":
        if key == "y":
            print("yes")
        elif key == "q":
            print("no")
        else:
            print("wrong key!")
    # itemPage.editDescriptions(replacement, summary="removing end full stop/period of the {}-description".format(key))


def sparqlQuery(query, site):

    generator = pg.WikidataSPARQLPageGenerator(query, site=site)

    for wd in generator:
        if (wd.exists()):
            wd.get(get_redirect=True)
            yield wd


def checkDesc(query, editMode):
    esCount = 0
    enCount = 0

    for item in sparqlQuery(query, site):
        itemPage = pywikibot.ItemPage(site, str(item).lstrip("[[wikidata:").rstrip("]]"))
        descriptions = item.descriptions
        for key in item.descriptions:
            try:
                if key == "es" or key == "en":
                    if item.descriptions["en"] is not "":
                        if item.descriptions["en"].endswith(".") is True:
                            pywikibot.logging.output("* Description:\t" + item.descriptions["en"])
                            replacement = re.sub("\\.$", "", item.descriptions["en"])
                            pywikibot.logging.output("* Replacement:\t" + replacement)
                            logging.basicConfig(filename='logs/itemDescFullStop.log', level=logging.INFO, format='* %(asctime)s » %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')

                            editItem(itemPage, replacement)

                            enCount += 1
                        else:
                            pass
                    elif item.descriptions["es"] is not "":
                        if item.descriptions["es"].endswith(".") is True:
                            pywikibot.logging.output("* Description:\t" + item.descriptions["es"])
                            replacement = re.sub("\\.$", "", item.descriptions["es"])
                            pywikibot.logging.output("* Replacement:\t" + replacement)
                            logging.basicConfig(filename='logs/itemDescFullStop.log', level=logging.INFO, format='* %(asctime)s » %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')

                            editItem(itemPage, replacement)

                            esCount += 1
                        else:
                            pass
                else:
                    pass
            except KeyError:
                pywikibot.logging.output("* KeyError:\t" + str(item) + key)
                logging.basicConfig(filename='logs/itemDescFullStop.log', level=logging.INFO, format='* %(asctime)s » %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')

    count = esCount + enCount
    print("Descriptions fixed: " + str(count))
    logging.basicConfig(filename='logs/itemDescFullStop.log', level=logging.INFO, format='* %(asctime)s » %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')


if __name__ == "__main__":
    rqFile = "fullStopsDescriptions.rq"
    with open("queries/" + rqFile, "r") as queryFile:
        query = queryFile.read()

    print("Do you want to run the script? y[es] or n[o] ")
    key = repr(readchar.readkey())
    key = key.replace("'", "")

    if key == "y":
        print("Starting script...")

        '''
        TO-DO: make the loop to decide if the user wants to run the script with
                or without edits (test mode/edit mode)
        '''

        edit = False

        checkDesc(query, edit)
    elif key == "n":
        print("Stopping script...")
        sys.exit()
    else:
        print("Wrong key!")

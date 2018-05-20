# -*- coding: utf-8 -*-

import pywikibot, re, datetime, logging, sys, inquirer
from pywikibot import pagegenerators as pg

site = pywikibot.Site("wikidata", "wikidata")


def editDesc(item, key, replacement):
    print("Edit mode not ready!")
    print("Decision: ")

    questions = [
        inquirer.List('actions',
            message="What do you want to do?",
            choices=['Remove full stop', 'Add description to checklist', 'Skip description', 'Quit'],
        ),
    ]

    answers = inquirer.prompt(questions)

    if answers["actions"] == "Remove full stop":
        print("TO-DO")
        # itemPage.editDescriptions(replacement, summary="removing end full stop/period of the {}-description".format(key))
    elif answers["actions"] == "Add description to checklist":
        print("TO-DO")
        # write a method to add the description with all its details in a CSV to review later
    elif answers["actions"] == "Skip description":
        print("{} ({}-desc) skipped\n".format(str(item).lstrip("[[wikidata:").rstrip("]]"), key))
        pass
    elif answers["actions"] == "Quit":
        print("Stopping bot...")
        edit = False

        return edit
    else:
        print("Something goes wrong...")


def sparqlQuery(query, site):

    generator = pg.WikidataSPARQLPageGenerator(query, site=site)

    for wd in generator:
        if (wd.exists()):
            wd.get(get_redirect=True)
            yield wd

def checkDesc(query, editMode):
    edit = True
    count = {
        "es": 0,
        "en": 0,
    }

    for item in sparqlQuery(query, site):
        if edit is not True:
            break
        else:
            itemPage = pywikibot.ItemPage(site, str(item).lstrip("[[wikidata:").rstrip("]]"))
            descriptions = item.descriptions
            for key in item.descriptions:
                try:
                    if key == "es" or key == "en":
                        if item.descriptions[key] is not "":
                            if item.descriptions[key].endswith(".") is True:
                                pywikibot.logging.output("* Description:\t" + item.descriptions[key])
                                replacement = re.sub("\\.$", "", item.descriptions[key])
                                pywikibot.logging.output("* Replacement:\t" + replacement)
                                logging.basicConfig(filename='logs/itemDescFullStop.log', level=logging.INFO, format='* %(asctime)s » %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')

                                edit = editDesc(itemPage, key, replacement)

                                count[key] += 1

                            else:
                                pass
                        else:
                            pass
                    else:
                        pass
                except KeyError:
                    pywikibot.logging.output("* KeyError:\t" + str(item) + key)
                    logging.basicConfig(filename='logs/itemDescFullStop.log', level=logging.INFO, format='* %(asctime)s » %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')

    resultCount = sum(count.values())
    print("Descriptions fixed: " + str(resultCount))
    print("Descriptions fixed by lang: " + str(count))

    logging.basicConfig(filename='logs/itemDescFullStop.log', level=logging.INFO, format='* %(asctime)s » %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')

    sys.exit()

if __name__ == "__main__":
    rqFile = "fullStopsDescriptions.rq"
    with open("queries/" + rqFile, "r") as queryFile:
        query = queryFile.read()

    question = [
        inquirer.Confirm("confirmation",
            message="Do you want to run the script?")
    ]

    answer = inquirer.prompt(question)

    if answer["confirmation"] is True:
        print("Starting script...")

        '''
        TO-DO: make the loop to decide if the user wants to run the script with
                or without edits (test mode/edit mode)
        '''

        edit = False

        checkDesc(query, edit)
    elif answer["confirmation"] is False:
        print("Stopping script...")
        sys.exit()
    else:
        print("Wrong key!")

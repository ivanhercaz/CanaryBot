# -*- coding: utf-8 -*-
from pywikibot import pagegenerators as pg
from pywikibot.editor import TextEditor

import colorama as c
import datetime
import inquirer
import logging
import pywikibot
import re
import sys

# Local modules
import bot

site = pywikibot.Site("wikidata", "wikidata")
cR = c.Style.RESET_ALL

# Just a help to have clear what it is pending yet.
TODO = c.Back.RED + c.Fore.WHITE + c.Style.BRIGHT + "TO-DO" + cR


def editDesc(item, key, description, replacement, count):
    questions = [
        inquirer.List('actions',
            message="What do you want to do?",
            choices=['Remove full stop', 'Add description to checklist', 'Edit description', 'Skip description', 'Quit'],
        ),
    ]

    answers = inquirer.prompt(questions)

    if answers["actions"] == "Remove full stop":
        print(TODO)
        count[key] += 1
        # itemPage.editDescriptions(replacement, summary="removing end full stop/period of the {}-description".format(key))
    elif answers["actions"] == "Add description to checklist":
        print(TODO)
        # write a method to add the description with all its details in a CSV to review later
    elif answers["actions"] == "Edit description":
        print(TODO)
        textEditor = TextEditor()
        # if the description has other error, the operator can edit it directly from the terminal
        # peding to do, it is just a test
        edit = textEditor.edit(description)

        # diff to check that everything is correct
        if edit and description != edit:
            pywikibot.showDiff(description, edit)

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
    # It is necessary to build the process in which the script edit if
    # the editMode is True
    edit = True
    lang = {
        "es": c.Back.RED + c.Fore.WHITE + c.Style.BRIGHT + "es-desc" + cR,
        "en": c.Back.BLUE + c.Fore.WHITE + c.Style.BRIGHT + "en-desc" + cR,
        "pl": c.Back.WHITE + c.Fore.RED + c.Style.BRIGHT + "pl-desc" + cR,
        "replacement": c.Style.BRIGHT + "Replacement" + cR
    }
    count = {
        "es": 0,
        "en": 0,
        "pl": 0
    }

    for item in sparqlQuery(query, site):
        if edit is False:
            break
        else:
            itemPage = pywikibot.ItemPage(site, str(item).lstrip("[[wikidata:").rstrip("]]"))
            descriptions = item.descriptions
            for key in item.descriptions:
                try:
                    if key == "es" or key == "en" or key == "pl":
                        if item.descriptions[key] is not "":
                            if item.descriptions[key].endswith(".") is True:
                                description = item.descriptions[key]
                                replacement = re.sub("\\.$", "", item.descriptions[key])

                                redFullStop = c.Fore.RED + c.Style.BRIGHT + "." + cR
                                item.descriptions[key] = re.sub("\\.$", redFullStop, item.descriptions[key])

                                pywikibot.logging.output("* " + lang[key] + ":\t" + item.descriptions[key])
                                pywikibot.logging.output("* " + lang["replacement"] + ":\t" + replacement + "\n")

                                logging.basicConfig(filename='logs/itemDescFullStop.log', level=logging.INFO, format='* %(asctime)s » %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')

                                edit = editDesc(itemPage, key, description, replacement, count)
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
        print("Starting script...\n")

        u = bot.Utilities()

        editMode = u.editMode()

        checkDesc(query, editMode)
    elif answer["confirmation"] is False:
        print("Stopping script...")
        sys.exit()
    else:
        print("Wrong key!")

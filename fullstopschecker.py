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
import log

site = pywikibot.Site("wikidata", "wikidata")
scriptName = "fullStopsChecker"

cR = c.Style.RESET_ALL

lang = {
    "es": c.Back.RED + c.Fore.WHITE + c.Style.BRIGHT + "es-desc" + cR,
    "en": c.Back.BLUE + c.Fore.WHITE + c.Style.BRIGHT + "en-desc" + cR,
    "pl": c.Back.WHITE + c.Fore.RED + c.Style.BRIGHT + "pl-desc" + cR,
}
misc = {
    "replace": c.Style.BRIGHT + "Replacement" + cR,
    "-": c.Fore.RED + "-" + cR,
    "+": c.Fore.GREEN + "+" + cR
}
count = {
    "es": 0,
    "en": 0,
    "pl": 0
}

now = datetime.datetime.now()
timestamp = str(now.strftime("%Y-%m-%d %H:%M"))


def setLogName():
    if editMode is True:
        script = scriptName
    else:
        script = scriptName + "-test"

    return script


def editDesc(itemPage, key, description, replacement, count, editMode, editGroup, logName):
    summary = {
        "removed": "removing end full stop/period of {}-desc".format(key),
        "edited": "removing end full stop/period and fixing {}-desc".format(key)
    }
    if editGroup is not None:
        summary = {
            "removed": "{} ([[:toollabs:editgroups/b/CB/{}|details]])".format(
                summary["removed"], editGroup
            ),
            "edited": "{} ([[:toollabs:editgroups/b/CB/{}|details]])".format(
                summary["edited"], editGroup
            )
        }

    item = str(itemPage).lstrip("[[wikidata:").rstrip("]]")

    questions = [
        inquirer.List('actions',
            message="What do you want to do?",
            choices=['Remove full stop', 'Add description to checklist', 'Edit description', 'Skip description', 'Quit'],
        ),
    ]

    answers = inquirer.prompt(questions)

    if answers["actions"] == "Remove full stop":
        count[key] += 1
        try:
            if editMode is True:
                info = u"{}{}{}{}\t{}\tfull stop removed".format(
                    c.Fore.WHITE, c.Style.BRIGHT, item, cR, lang[key]
                )
                print(info)
                info = {
                    "time": timestamp,
                    "item": item,
                    "key": key + "-desc",
                    "msg": "full stop removed"
                }
                itemPage.editDescriptions(replacement, summary=summary["removed"])
                log.check(info, logName, mode="csv")
            else:
                info = u"{}{}{}{}\t{}\tfull stop removed (non edit made, test mode)".format(
                    c.Fore.WHITE, c.Style.BRIGHT, item, cR, lang[key]
                )
                print(info)
                info = {
                    "time": timestamp,
                    "item": item,
                    "key": key + "-desc",
                    "msg": "full stop removed (non edit made, test mode)"
                }
                log.check(info, logName, mode="csv")

        except Exception as e:
            print(e)
            log.check(e, logName, mode="csv")
    elif answers["actions"] == "Add description to checklist":
        info = {
            "time": timestamp,
            "item": item,
            "key": key + "-desc",
            "msg": description
        }
        log.check(info, "descriptionCheckList", mode="csv")
    elif answers["actions"] == "Edit description":
        textEditor = TextEditor()
        # if the description has other error, the operator can edit it directly from the terminal
        # peding to do, it is just a test
        newDescription = textEditor.edit(description)

        # diff to check that everything is correct
        if newDescription and description != newDescription:
            pywikibot.showDiff(description, newDescription)

            question = [
                inquirer.Confirm("confirmation",
                    message="Are you sure you want to make this change?")
            ]

            answer = inquirer.prompt(question)

            if answer["confirmation"] is True:
                if editMode is True:
                    info = u"{}{}{}{}\t{}\tfull stop removed and other errors fixed".format(
                        c.Fore.WHITE, c.Style.BRIGHT, item, cR, lang[key]
                    )
                    print(info)
                    info = {
                        "time": timestamp,
                        "item": item,
                        "key": key + "-desc",
                        "msg": "full stop removed and other errors fixed"
                    }
                    itemPage.editDescriptions(replacement, summary=summary["edited"])
                    log.check(info, logName, mode="csv")
                else:
                    info = u"{}{}{}{}\t{}\tfull stop removed and other errors fixed (test mode)".format(
                        c.Fore.WHITE, c.Style.BRIGHT, item, cR, lang[key]
                    )
                    print(info)
                    info = {
                        "time": timestamp,
                        "item": item,
                        "key": key + "-desc",
                        "msg": "full stop removed and other errors fixed (test mode)"
                    }
                    log.check(info, logName, mode="csv")
            else:
                info = u"{}{}{}{}\t{}The change hasn't been made by decision of the operator.".format(
                    c.Fore.WHITE, c.Style.BRIGHT, item, cR, lang[key]
                )
                print(info)
                info = {
                    "time": timestamp,
                    "item": item,
                    "key": key + "-desc",
                    "msg": "The change hasn't been made by decision of the operator"
                }
                log.check(info, logName, mode="csv")
        else:
            print("No changes were made.")

    elif answers["actions"] == "Skip description":
        info = u"{}{}{}{}\t{}\tskipped.".format(
            c.Fore.WHITE, c.Style.BRIGHT, item, cR, lang[key]
        )
        print(info)
        info = {
            "time": timestamp,
            "item": item,
            "key": key + "-desc",
            "msg": "skipped"
        }
        log.check(info, logName, mode="csv")
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

    editGroup = u.editGroups()

    # It is necessary to build the process in which the script edit if
    # the editMode is True
    edit = True

    logName = setLogName()

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

                                print("\n   {}{}{}{}".format(
                                    c.Fore.WHITE, c.Style.BRIGHT, str(item).lstrip("[[wikidata:").rstrip("]]"), cR)
                                )
                                print(" {} {}:\t{}".format(misc["-"], lang[key], item.descriptions[key]))
                                print(" {} {}:\t{}\n".format(misc["+"], misc["replace"], replacement))

                                edit = editDesc(itemPage, key, description, replacement, count, editMode, editGroup, logName)
                            else:
                                pass
                        else:
                            pass
                    else:
                        pass
                except KeyError as e:
                    item = str(item).lstrip("[[wikidata:").rstrip("]]")
                    info = u"{}\t{}-desc\tKeyError: {}".format(item, key, e)
                    print(info)
                    info = {
                        "item": item,
                        "key": key + "-desc",
                        "msg": e
                    }

                    log.check(info, logName, mode="csv")

    resultCount = sum(count.values())
    fixed = "Descriptions fixed: {}. ".format(str(resultCount))
    fixedByLang = "Descriptions fixed by lang: {}".format(str(count))
    item = str(item).lstrip("[[wikidata:").rstrip("]]")

    if edit is False:
        info = "Interruption of the script by the operator.\n{}\n{}".format(
            fixed, fixedByLang
        )
        print(info)
        info = {
            "time": timestamp,
            "item": item,
            "key": key + "-desc",
            "msg": "Interruption of the script by the operator. " + fixed + fixedByLang
        }
    else:
        info = "Task completed!\n{}\n{}".format(
            fixed, fixedByLang
        )
        print(info)
        info = {
            "time": now.strftime("%Y-%m-%d %H:%M"),
            "item": item,
            "key": key + "-desc",
            "msg": "Task completed!\n" + fixed + "\n" + fixedByLang
        }

    log.check(info, logName, mode="csv", generateHTML=True)
    log.check(info, "descriptionCheckList", mode="csv", generateHTML=True)

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

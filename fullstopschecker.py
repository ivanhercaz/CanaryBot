# -*- coding: utf-8 -*-
# fullstopschecker.py
# Distributed under the terms of the GNU General Public License v3.0
'''
Script to remove all the full stops/periods of the descriptions in Wikidata items.

The script run a SPARQL query in the Wikidata Query Service (WDQS) and then it check
if the description meets the requirements: confirm that end with ".", check only the
descriptions in the languages in which the bot has been configured, and if the full
stop is not part of an exception (e.g. abbreviatures as w. in Polish or a. C. in
Italian or Spanish). When the description meets the requirements there are five options:
    1. Remove the full stop.
    2. Add description to checklist.
        It means to add the description to another CSV file. This checlist serves
        to configure the exceptions list to avoid in the next run some of the descriptions.
    3. Edit description.
        It serves when the description has been vandalized or there is another error
        easy to solve.
    4. Skip.
    5. Quit.

Each action is checked and registered in a CSV log in /logs and, at the end, it generates
a HTML file that works as CSV viewer (the same if a CSV checklist has been created).
'''
import colorama as c
import csv
import datetime
import inquirer
import re
import sys

# Pywikibot
import pywikibot
from pywikibot import pagegenerators as pg
from pywikibot.editor import TextEditor

# Local modules
import log
import utils as u

# Configuration
site = pywikibot.Site("wikidata", "wikidata")
scriptName = "fullStopsChecker"
now = datetime.datetime.now()
timestamp = str(now.strftime("%Y-%m-%d %H:%M"))

# Colorama reset
cR = c.Style.RESET_ALL

'''
If you want the bot to change descriptions in other languages, you can open an issue
in the GitHub repository. Or, you can read the next instructions to add yourself
the code.

Instructions to add another language in the code.
    1. In "lang" dictionary you have to:
        1. Write a comma at the end of the last key-value.
        2. In another line configure the language with the format:
            "key": c.Back.COLOR + c.Fore.COLOR + c.Style.BRIGHT + "key-desc" + cR
            The colors available are:
                - Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
                - Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
                - Style: DIM, NORMAL, BRIGHT, RESET_ALL
        3. Then, in "count" dictionary, you have to write the comma at the end of
        the last key-value and in another line:
            "key": 0
        4. Then, open a pull request with the change in the GitHub repository.
        5. This is enoug for me to configure the rest of the bot to work in the
        language you have set, but you can also change the first "if" of the "try"
        statement, adding:
            key == "key-lang"
'''
# Key languages for the descriptions that the bot change.
# This key languages has a background color (c.Back.X), a foreground color (c.Fore.X)
# a style (c.Style.X) and the Colorama reset to make more pleasant the work in the cli.
lang = {
    "es": c.Back.RED + c.Fore.WHITE + c.Style.BRIGHT + "es-desc" + cR,
    "en": c.Back.BLUE + c.Fore.WHITE + c.Style.BRIGHT + "en-desc" + cR,
    "pl": c.Back.WHITE + c.Fore.RED + c.Style.BRIGHT + "pl-desc" + cR,
    "it": c.Back.GREEN + c.Fore.WHITE + c.Style.BRIGHT + "it-desc" + cR
}

# Counters (set in 0 at the beginning of the script).
count = {
    "es": 0,
    "en": 0,
    "pl": 0,
    "it": 0
}

# Some colored useful words or symbols.
misc = {
    "replace": c.Style.BRIGHT + "Replacement" + cR,
    "-": c.Fore.RED + "-" + cR,
    "+": c.Fore.GREEN + "+" + cR
}

# List of regular expressions to make exceptions (don't remove full stops when it
# is part of...)
exceptions = [
    # regex for: a. C., a.C., d.C., d. C., S.A., etc.
    re.compile(r"\w\.\s?\w\.$"),
    # regex for: Jr., Sr.
    re.compile(r"\s(J|S)r\.$"),
    # regex for: r. (Polish abbreviature for "in YEAR").
    re.compile(r"\sr\.$"),
    # regex for: w. (Polish abbreviature for "in YEAR").
    re.compile(r"\sw\.$"),
    # regex for: Inc., Co., and Ltd. (suffix indicating a corporation).
    re.compile(r"\s(Inc|Co|Ltd)\.$"),
    # regex for: EE.UU., EE. UU., U.S.A., U. S. A., U.S., U. S.
    re.compile(r"\s(EE\.\s?UU\.|U\.\s?S\.\s?A\.|U\.\s?S\.)$")
]

dataIndex = -1
duplicated = "duplicatedFullStopsDesc.csv"

def setLogName(editMode):
    """Simple function to set the name of the log according to the editing mode.

    Returns
    -------
    string
        log name with the form of "scriptName" if the script is going to edit, or
        "scriptName-test" if the script is running in test mode.

    """
    if editMode is True:
        script = scriptName
    else:
        script = scriptName + "-test"

    return script


def editDesc(itemPage, key, description, newDescription, count, editMode, editGroup, logName):
    """Provides the available options and executes the corresponding editions.

    Parameters
    ----------
    itemPage : string
        Wikidata item.
    key : string
        language of the description with a fulls stop.
    description : string
        the description with the full stop.
    newDescription : string
        the description without the full stop
    count : integer
        counter incremented by 1
    editMode : boolean
        editing mode, False for test edits or True to enable the editing.
    editGroup : boolean
        if it is true, generate a hash to identify the EditGroup,
        check: https://tools.wmflabs.org/editgroups
    logName : string
        name of the logfile.

    Returns
    -------
    string
        edition

    """
    replacement = {
        key: newDescription
    }

    # Summaries for the action of "remove full stop" and for "Edit description"
    # respectively
    summary = {
        "removed": "removing end full stop/period of {}-desc".format(key),
        "edited": "removing end full stop/period and fixing {}-desc".format(key)
    }

    # Check if the operator choose to create an EditGroup and change the Summaries
    # according to the decision
    if editGroup is not None:
        summary = {
            "removed": "{} ([[:toollabs:editgroups/b/CB/{}|details]])".format(
                summary["removed"], editGroup
            ),
            "edited": "{} ([[:toollabs:editgroups/b/CB/{}|details]])".format(
                summary["edited"], editGroup
            )
        }

    # Item identifier formatted
    item = str(itemPage).lstrip("[[wikidata:").rstrip("]]")

    if description in duplicated:
        try:
            # Check the editing mode
            if editMode is True:
                # Information string to print in the cli
                info = u"{}{}{}{}\t{}\tfull stop removed automatically".format(
                    c.Fore.WHITE, c.Style.BRIGHT, item, cR, lang[key]
                )
                print(info)

                # Information dictionary to make the log (without Colorama)
                info = {
                    "time": timestamp,
                    "item": item,
                    "key": key + "-desc",
                    "msg": "full stop removed automatically"
                }

                # Applying the edition
                itemPage.editDescriptions(replacement, summary=summary["removed"])

                # Checking and updating the CSV logfile
                log.check(info, logName, mode="csv")

            else:
                info = u"{}{}{}{}\t{}\tfull stop removed automatically(non edit made, test mode)".format(
                    c.Fore.WHITE, c.Style.BRIGHT, item, cR, lang[key]
                )
                print(info)

                info = {
                    "time": timestamp,
                    "item": item,
                    "key": key + "-desc",
                    "msg": "full stop removed automatically (non edit made, test mode)"
                }

                log.check(info, logName, mode="csv")

        except Exception as e:
            print(e)

            info = {
                "time": timestamp,
                "item": item,
                "key": key + "-desc",
                "msg": e
            }

            log.check(info, logName, mode="csv")

    # Ask for the correct action
    questions = [
        inquirer.List('actions',
            message="What do you want to do?",
            choices=['Remove full stop', 'Add description to checklist', 'Edit description', 'Remove duplicates automatically', 'Skip description', 'Quit'],
        ),
    ]

    answers = inquirer.prompt(questions)

    # Remove full stop
    if answers["actions"] == "Remove full stop":
        count[key] += 1
        try:
            # Check the editing mode
            if editMode is True:
                # Information string to print in the cli
                info = u"{}{}{}{}\t{}\tfull stop removed".format(
                    c.Fore.WHITE, c.Style.BRIGHT, item, cR, lang[key]
                )
                print(info)

                # Information dictionary to make the log (without Colorama)
                info = {
                    "time": timestamp,
                    "item": item,
                    "key": key + "-desc",
                    "msg": "full stop removed"
                }

                # Applying the edition
                itemPage.editDescriptions(replacement, summary=summary["removed"])

                # Checking and updating the CSV logfile
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

            info = {
                "time": timestamp,
                "item": item,
                "key": key + "-desc",
                "msg": e
            }

            log.check(info, logName, mode="csv")

    # Add description to checklist.
    elif answers["actions"] == "Add description to checklist":
        info = {
            "time": timestamp,
            "item": item,
            "key": key + "-desc",
            "msg": "Added to checklist: " + description
        }

        # It doesn't edit the item description, it just add the info to the logfile
        log.check(info, logName, mode="csv")
        # And update the checklist to review manually later.
        log.check(info, "descriptionCheckList", mode="csv")

    # Edit description
    elif answers["actions"] == "Edit description":
        # If the description has other error, the operator can edit it directly
        # from the terminal
        textEditor = TextEditor()
        newDescription = textEditor.edit(description)

        # Diff to check that everything is correct
        if newDescription and description != newDescription:
            pywikibot.showDiff(description, newDescription)

            question = [
                inquirer.Confirm("confirmation",
                    message="Are you sure you want to make this change?")
            ]

            answer = inquirer.prompt(question)

            # If the operator confirm the change...
            if answer["confirmation"] is True:
                try:
                    # Check the editing mode
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

                except Exception as e:
                    print(e)

                    info = {
                        "time": timestamp,
                        "item": item,
                        "key": key + "-desc",
                        "msg": e
                    }

                    log.check(info, logName, mode="csv")

            # If the operator doesn't confirm the change
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

    # Remove if the script find the same description again
    elif answers["actions"] == "Remove duplicates automatically":
        global dataIndex
        dataIndex += 1

        with open(duplicated, "r+") as duplicatedFile:
            reader = csv.reader(duplicatedFile, delimiter=",")
            for row in reader:
                if description not in row[1]:
                    writer = csv.writer(duplicatedFile, delimiter=",")
                    writer.writerow([dataIndex, description])
                    print("Duplicated description added to the file.")

                    try:
                        # Check the editing mode
                        if editMode is True:
                            # Information string to print in the cli
                            info = u"{}{}{}{}\t{}\tfull stop removed automatically".format(
                                c.Fore.WHITE, c.Style.BRIGHT, item, cR, lang[key]
                            )
                            print(info)

                            # Information dictionary to make the log (without Colorama)
                            info = {
                                "time": timestamp,
                                "item": item,
                                "key": key + "-desc",
                                "msg": "full stop removed automatically"
                            }

                            # Applying the edition
                            itemPage.editDescriptions(replacement, summary=summary["removed"])

                            # Checking and updating the CSV logfile
                            log.check(info, logName, mode="csv")

                        else:
                            info = u"{}{}{}{}\t{}\tfull stop removed automatically(non edit made, test mode)".format(
                                c.Fore.WHITE, c.Style.BRIGHT, item, cR, lang[key]
                            )
                            print(info)

                            info = {
                                "time": timestamp,
                                "item": item,
                                "key": key + "-desc",
                                "msg": "full stop removed automatically (non edit made, test mode)"
                            }

                            log.check(info, logName, mode="csv")

                    except Exception as e:
                        print(e)

                        info = {
                            "time": timestamp,
                            "item": item,
                            "key": key + "-desc",
                            "msg": e
                        }

                        log.check(info, logName, mode="csv")

    # Skip description
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

    # Quit
    elif answers["actions"] == "Quit":
        print("Stopping bot...")
        # Set "edit" as False to stop the script
        edit = False

        return edit

    else:
        print("Something goes wrong...")


def sparqlQuery(query, site):
    """Run a SPARQL Query in WDQS.

    Parameters
    ----------
    query : string
        query to run
    site : string
        the site to perform the query

    Returns
    -------
    generator
        items in the query

    """
    generator = pg.WikidataSPARQLPageGenerator(query, site=site)

    # For each item (wd) in the SPARQL query (generator)
    for wd in generator:
        if (wd.exists()):
            wd.get(get_redirect=True)
            yield wd


def checkDesc(query, editMode):
    """Check if the description meet the requirements and show it to the operator.

    Parameters
    ----------
    query : string
        query to run
    editMode : boolean
        editing mode, False for test edits or True to enable the editing.

    """
    # Ask about the necessity to create an EditGroup for this task
    editGroup = u.editGroups()

    # When "edit" is True, the script will be running until something or the operator
    # stop it. If the operator choose "Quit", "edit" will be returned as "False"
    edit = True

    # To set the log name depending of the editing mode
    logName = setLogName(editMode)

    for item in sparqlQuery(query, site):
        # If "edit" is False, stop the script
        if edit is False:
            break

        else:
            descriptions = item.descriptions
            # Check the key of the languages in the descriptions of the item
            for key in descriptions:
                try:
                    # If the description is in one of the languagesof the lang dictionary (at the beginning)...
                    if key in lang:
                        # And if it isn't empty...
                        if item.descriptions[key] is not "":
                            # And if it ends with a dot...
                            if item.descriptions[key].endswith(".") is True:
                                # And it doesn't match any exception...
                                if not any(exception.search(item.descriptions[key]) for exception in exceptions):
                                    # Setting variables to pass to editDesc()
                                    description = item.descriptions[key]
                                    newDescription = re.sub(r"\s?\.$", "", item.descriptions[key])

                                    # Show the full stop in red
                                    redFullStop = c.Fore.RED + c.Style.BRIGHT + "." + cR
                                    item.descriptions[key] = re.sub(r"\s?\.$", redFullStop, item.descriptions[key])

                                    print("\n   {}{}{}{}\t{}".format(
                                        c.Fore.WHITE, c.Style.BRIGHT, str(item).lstrip("[[wikidata:").rstrip("]]"), cR,
                                        item.labels[key])
                                    )
                                    print(" {} {}:\t{}".format(misc["-"], lang[key], item.descriptions[key]))
                                    print(" {} {}:\t{}\n".format(misc["+"], misc["replace"], newDescription))

                                    # Make the choice
                                    edit = editDesc(item, key, description, newDescription, count, editMode, editGroup, logName)

                                # If not, pass...
                                else:
                                    pass
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

    # Statistics
    # Descriptions fixed
    resultCount = sum(count.values())
    fixed = "Descriptions fixed: {}. ".format(str(resultCount))
    # Descriptions fixed by lang
    fixedByLang = "Descriptions fixed by lang: {}".format(str(count))

    item = str(item).lstrip("[[wikidata:").rstrip("]]")

    # Check if the bot is stopped by the operator...
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

    # Or if the query end...
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

    # Generate CSV viewer for the logfile
    log.check(info, logName, mode="csv", generateHTML=True)
    # Generate the CSV viewer for the checklist
    log.check(info, "descriptionCheckList", mode="csv", generateHTML=True)

    # The end!
    sys.exit()


if __name__ == "__main__":
    # Query file
    rqFile = "fullStopsDescriptions.rq"

    # Reading the query
    with open("queries/" + rqFile, "r") as queryFile:
        query = queryFile.read()

    print("Starting script...\n")

    # Ask for the edit mode (test or not)
    editMode = u.editMode()

    # Run the script
    checkDesc(query, editMode)

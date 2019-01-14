# -*- coding: utf-8 -*-
import colorama as c
import datetime
import inquirer
import os
import random

# Local modules
import utils as u
import fullstopschecker as fsc
import setlabeldesc as sld
# import setlabeldescalias as slda

cR = c.Style.RESET_ALL

def massiveDesc(edit):
    ''' Prepare the execution of setlabeldesc.py
        Add labels and description to an item given an specific source lang'''

    queriesAnswer = u.checkQueries()

    questions = [
        inquirer.Text("desc", message="Escribe la descripción que quieres añadir"),
        inquirer.Text("lang", message="¿En qué idioma está la descripción que quieres introducir?"),
        inquirer.Text("sourceLang", message="¿De que idioma quieres trabajar y copiar la etiqueta?")
    ]

    answers = inquirer.prompt(questions)
    desc = answers["desc"]
    lang = answers["lang"]
    sourceLang = answers["sourceLang"]

    try:
        print("\nSe ejecutará la consulta {}".format(queriesAnswer))

        with open("queries/" + queriesAnswer, "r") as queryFile:
            query = queryFile.read()

        sld.setLabel(query, desc, lang, sourceLang, edit)
    except FileNotFoundError:
        print("\nThe query {} does not exist".format(queriesAnswer))
        print(u"\nThis file does not exist Create it or enter another name.")


def setLabelDescAlias(edit):
    print("Preparing the script!")


def removeFullStop(edit):
    print("Preparing the script!")

    rqFile = "fullStopsDescriptions.rq"

    try:
        print("\nSe ejecutará la consulta {}".format(rqFile))

        with open("queries/" + rqFile, "r") as queryFile:
            query = queryFile.read()

        fsc.checkDesc(query, edit)
    except FileNotFoundError:
        print("\nLa consulta {} no existe".format(queriesAnswer))
        print(u"No existe ese archivo. Créalo o introduce otro nombre.")


if __name__ == '__main__':
    now = datetime.datetime.now()

    print(c.Fore.CYAN + "Hoy es " + now.strftime("%d-%m-%Y %H:%M") + cR)
    print("\n― Panel de control de Canary Bot")
    print("""
       _;;;       ___   __   _   _   __    ____  _   _
      /  · >     |     /  \  |\  |  /  \  |    )  \ /    ____   __  _____
  __ / /   )     |    |____| | \ | |____| |---/    |    |____) |  |   |
  \__\/___/      |___ |    | |  \| |    | |   \    |    |____) |__|   |
      | |
      ^ ^
  ------------------------------------------------------------------------
    """)

    projects = [
        inquirer.List("projects",
            message="Proyectos disponibles:",
            choices=["eswiki", "testwiki", "wikidata", "testwikidata"],
        ),
    ]

    answers = inquirer.prompt(projects)
    
    edit = u.editMode()

    if answers["projects"] == "eswiki":
        tasks = {
            inquirer.List("eswikiTasks",
                message="Tareas disponibles:",
                choices=["Control de autoridades", "Sustituir multimedia"],
            ),
        }

        print("Aún no están preparados los scripts")

    elif answers["projects"] == "testwiki":
        tasks = {
            inquirer.List("testwikiTaks",
                message="Tareas disponibles:",
                choices=["Control de autoridades", "Sustituir multimedia"],
            ),
        }

        print("Aún no están preparados los scripts")

    elif answers["projects"] == "wikidata":
        tasks = {
            inquirer.List("wikidata",
                message="Tareas disponibles:",
                choices=["Descripciones de un idioma a otro", "Retirar punto y final a las descripciones",
                        "..."],
            ),
        }

        answers = inquirer.prompt(tasks)

        print("Aún no están preparados los scripts")

        if answers["wikidata"] == "Descripciones de un idioma a otro":
            massiveDesc(edit)
        elif answers["wikidata"] == "Retirar punto y final a las descripciones":
            removeFullStop(edit)
        else:
            print("error -:::-")

    elif answers["projects"] == "testwikidata":
        tasks = {
            inquirer.List("testwikidata",
                message="Tareas disponibles:",
                choices=["SetLabelDescAlias",
                    "..."],
            ),
        }

        answers = inquirer.prompt(tasks)

        if answers["testwikidata"] == "SetLabelDescAlias":
            setLabelDescAlias()
        else:
            print("error -:::-")
    else:
        print("¡Algo no fue como debía!")

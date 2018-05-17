# -*- coding: utf-8 -*-
import colorama as c
import datetime, sys, os, inquirer, os
import setlabeldesc as sld
import setlabeldescalias as slda
from pathlib import Path
# Pywikibot is executed in each script

cR = c.Style.RESET_ALL


def editMode():
    ''' Function to work like an easy and clean way to choose the edition mode,
    otherwhise this could would have in each one '''

    editMode = [
        inquirer.List("editMode",
            message="Elige el modo de edición",
            choices=["Modo de pruebas", "Modo editar"],
        ),
    ]

    answers = inquirer.prompt(editMode)

    if answers["editMode"] == u"Modo editar":
        edit = True
        return edit


def massiveDesc():
    ''' Prepare the execution of setlabeldesc.py
        Add labels and description to an item given an specific source lang'''

    edit = editMode()

    # Checking filenames
    f = []

    for (dirs, dirsNames, files) in os.walk("queries"):
        f.extend(files)
        for filename in enumerate(files):
            filenames = filename
            print(filenames)

    print("Hay {} consultas disponibles.\n".format(len(files)))

    queries = [
        inquirer.List("queries",
            message="Qué consulta quieres utilizar?",
            choices=files
        ),
    ]

    queriesAnswer = inquirer.prompt(queries)
    queriesAnswer = str(queriesAnswer)
    queriesAnswer = queriesAnswer[13:].strip("'}")
    fileQuery = Path("queries/{}".format(queriesAnswer))

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
        print("\nLa consulta {} no existe".format(queriesAnswer))
        print(u"No existe ese archivo. Créalo o introduce otro nombre.")


def setLabelDescAlias():
    print("Preparing the script!")


def removeFullStop():
    print("Preparing the script!")


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
            massiveDesc()
        elif answers["wikidata"] == "Retirar punto y final a las descripciones":
            removeFullStop()
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

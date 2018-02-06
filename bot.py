# -*- coding: utf-8 -*-
import colorama as c
import datetime, sys, os, inquirer, os
import setlabeldesc as sld
# import setlabeldesc as sld
# Pywikibot is executed in each script

cR = c.Style.RESET_ALL

def editMode():
    editMode = [
        inquirer.List("editMode",
            message = "Elige el modo de edición",
            choices = ["Modo de pruebas", "Modo editar"],
        ),
    ]

    answers = inquirer.prompt(editMode)

    if answers["editMode"] == u"Modo editar":
        edit = True
        return edit

def massiveDesc():
    edit = editMode()
    for root, dirs, files in os.walk("queries"):
        for filename in files:
            print(filename)

    queries = [
        inquirer.List("queries",
            message = "Qué consulta quieres utilizar?",
            choices = files
        ),
    ]

    queriesAnswer = inquirer.prompt(queries)

    questions = [
        inquirer.Text("desc", message = "Escribe la descripción que quieres añadir"),
        inquirer.Text("lang", message = "¿En qué idioma está la descripción que quieres introducir?"),
        inquirer.Text("sourceLang", message = "¿De que idioma quieres trabajar y copiar la etiqueta?")
    ]

    answers = inquirer.prompt(questions)
    desc = answers["desc"]
    lang = answers["lang"]
    sourceLang = answers["sourceLang"]

    if queriesAnswer["queries"] == filename:
        print("Fine!")

        with open("queries/" + filename, "r") as queryFile:
            query = queryFile.read()

        sld.setLabel(query, desc, lang, sourceLang, edit)
    else:
        print(u"No existe ese archivo. Créalo o introduce otro nombre.")

def removeEndPoint():
    print("Test EndPoint")

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
            message = "Proyectos disponibles:",
            choices = ["eswiki", "testwiki", "wikidata", "testwikidata"],
        ),
    ]

    answers = inquirer.prompt(projects)

    if answers["projects"] == "eswiki":
        tasks = {
            inquirer.List("eswikiTasks",
                message = "Tareas disponibles:",
                choices = ["Control de autoridades", "Sustituir multimedia"],
            ),
        }

        print("Aún no están preparados los scripts")

    elif answers["projects"] == "testwiki":
        tasks = {
            inquirer.List("testwikiTaks",
                message = "Tareas disponibles:",
                choices = ["Control de autoridades", "Sustituir multimedia"],
            ),
        }

        print("Aún no están preparados los scripts")

    elif answers["projects"] == "wikidata":
        tasks = {
            inquirer.List("wikidata",
                message = "Tareas disponibles:",
                choices = ["Descripciones de un idioma a otro", "Retirar punto y final a las descripciones",
                            "..."],
            ),
        }

        answers = inquirer.prompt(tasks)

        print("Aún no están preparados los scripts")

        if answers["wikidata"] == "Descripciones de un idioma a otro":
            massiveDesc()
        else:
            print("error -:::-")

    elif answers["projects"] == "testwikidata":
        tasks = {
            inquirer.List("testwikidata",
                message = "Tareas disponibles:",
                choices = ["Descripciones de un idioma a otro", "Retirar punto y final a las descripciones",
                            "..."],
            ),
        }

        print("Aún no están preparados los scripts")
    else:
        print("¡Algo no fue como debía!")

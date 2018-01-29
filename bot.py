# -*- coding: utf-8 -*-
import colorama as c
import datetime, sys, os, inquirer
# Pywikibot is executed in each script

cR = c.Style.RESET_ALL

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

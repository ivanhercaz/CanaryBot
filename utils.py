import inquirer
import os
import random

''' Module  for useful snippets '''

def editGroups():
    ''' Method to check if the operator wants to create a set of changes in
    Edit groups. Check: https://www.wikidata.org/wiki/Wikidata:Edit_groups '''

    question = [
        inquirer.Confirm("editGroups",
            message="Do you want to track edits in a set of Edit groups?",
            )
    ]

    answer = inquirer.prompt(question)

    if answer["editGroups"] is True:
        editGroup = "{:x}".format(random.randrange(0, 2**48))
        return editGroup

def editMode():
    ''' Method to work like an easy and clean way to choose the edition mode,
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

def checkQueries():
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

    return queriesAnswer


def setLogName(editMode, scriptName):
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



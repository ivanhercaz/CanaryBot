# -*- coding: utf-8 -*-
import datetime, inquirer, logging, os

def update(info, fullNameLog, dateTime):
    print(fullNameLog)
    print("\nActualizando log...")

    logging.basicConfig(
        filename = fullNameLog,
        level = logging.INFO,
        format = "%(asctime)s » %(message)s",
        datefmt = "%d/%m/%Y %I:%M:%S %p"
    )
    logging.info(info)

    print(dateTime + " » " + info)

def check(info, key, script):
    logDir = "logs/"
    now = datetime.datetime.now()
    nowFormat = now.strftime("%Y-%m-%d %H:%M")

    if key == "":
        nameLog = script
    else:
        nameLog = "-" + key + "-" + script

    fullNameLog = logDir + nowFormat + nameLog + ".log"

    if os.path.exists(logDir):
        update(info, fullNameLog, nowFormat)
    else:
        print(logDir + " creado")
        os.makedirs(logDir)
        update(info, fullNameLog, nowFormat)

def ask(info="", script = "script desconocido"):
    # Ternary operation to make a default info text if there isn't info provided
    info = "No se ha aportado información sobre lo ocurrido" if (info == "") else info

    nameQuestion = [
        inquirer.List("nameLog", message = u"¿Quieres añadirle alguna palabra clave al nombre del log?",
                        choices = [u"Sí", u"No"])
    ]

    answers = inquirer.prompt(nameQuestion)

    # Check if it's necessary some extra keyword to identify the log file
    if answers["nameLog"] == u"Sí":
        nameQuestion = [
            inquirer.Text("keyName", message = "¿Qué palabra clave?")
        ]

        answers = inquirer.prompt(nameQuestion)

        keyName = answers["keyName"]

        print(u"\nSe utilizará el siguiente nombre: año-mes-día_hora:minutos-" + keyName + "-" + script + ".log")
        check(info, keyName, script)
    else:
        # There isn't any keyname, so just enter two args
        check(info, key = "", script = "")

# This is here to test the module by default, without the necessity to make changes in any script file.
# When the module will be fine tested and ready to use in the scripts, this will be deleted.
ask()

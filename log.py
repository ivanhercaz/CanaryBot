# -*- coding: utf-8 -*-
import datetime, inquirer, logging, os

def update(fullNameLog):
    print("\nActualizando log...")
    logging.basicConfig(
        filename = fullNameLog,
        level = logging.INFO,
        format = "%(asctime)s » %(message)s",
        datefmt = "%d/%m/%Y %I:%M:%S %p"
    )

def check(key, script):
    logDir = "logs/"
    now = datetime.datetime.now()
    nowFormat = now.strftime("%Y-%m-%d_%H:%M")

    if key == "":
        nameLog = script
    else:
        nameLog = key + "-" + script

    fullNameLog = logDir + nowFormat + "-" + nameLog

    if os.path.exists(logDir):
        update(fullNameLog)
    else:
        print(logDir + " creado")
        os.makedirs(logDir)
        update(fullNameLog)

def ask(script = ""):
    nameQuestion = [
        inquirer.List("nameLog", message = u"¿Quieres añadirle alguna palabra clave al nombre del log?",
                        choices = [u"Sí", u"No"])
    ]

    answers = inquirer.prompt(nameQuestion)

    if answers["nameLog"] == u"Sí":
        nameQuestion = [
            inquirer.Text("keyName", message = "¿Qué palabra clave?")
        ]

        answers = inquirer.prompt(nameQuestion)

        keyName = answers["keyName"]

        print(u"\nSe utilizará el siguiente nombre: año-mes-día_hora:minutos-" + keyName + "-" + script + ".log")
        check(keyName, script)
    else:
        check()

ask()

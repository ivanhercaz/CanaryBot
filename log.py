# -*- coding: utf-8 -*-
import datetime, inquirer, logging, os

def update(info, fullNameLog, dateTime):
    print("\nActualizando log...")

    logging.basicConfig(
        filename = fullNameLog,
        level = logging.INFO,
        format = u"%(asctime)s » %(message)s",
        datefmt = "%d/%m/%Y %I:%M:%S %p"
    )
    logging.info(info)

    print(dateTime + u" » " + info)

    return fullNameLog, dateTime

def check(info, script):
    # Checking format of the name log

    logDir = "logs/"
    now = datetime.datetime.now()
    nowFormat = now.strftime("%Y-%m-%d %H:%M")

    fullNameLog = logDir + nowFormat + script + ".log"

    if os.path.exists(logDir):
        update(info, fullNameLog, nowFormat)
    else:
        print(logDir + " creado")
        os.makedirs(logDir)
        update(info, fullNameLog, nowFormat)

# This is here to test the module by default, without the necessity to make changes in any script file.
# When the module will be fine tested and ready to use in the scripts, this will be deleted.
# ask()

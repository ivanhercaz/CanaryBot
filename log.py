# -*- coding: utf-8 -*-
import csv
import datetime
import inquirer
import logging
import pywikibot
import os


def update(info, fullNameLog, dateTime, mode="log"):
    """Update the log file.

    Parameters
    ----------
    info : string
        Message to record the action in the log file.
    fullNameLog : string
        File address where is the logfile and its included.
    dateTime : datetime
        Exact moment in which the action described in 'info' occured.

    Returns
    -------
    tuple
        fullNameLog and dateTime variables.

    """
    print("\nUpdating log...\n")

    if mode == "log":
        # Configuration
        logging.basicConfig(
            filename=fullNameLog,
            level=logging.INFO,
            format=u"%(asctime)s\t%(message)s",
            datefmt="%d/%m/%Y %I:%M:%S %p"
        )

        # Updating log
        logging.info(info)
    if mode == "csv":
        with open(fullNameLog, "a") as csvFile:
            print(info)
            row = info["item"], info["key"], info["msg"]
            writer = csv.writer(csvFile, lineterminator="\n")
            writer.writerow(row)
    else:
        print("Something goes wrong with the mode of the log")

    return fullNameLog, dateTime


def check(info, script, mode="log"):
    """Check if the directory is available or if it has to be created,
        also assign a date and time (now) in which the actions has been logged.

    Parameters
    ----------
    info : string
        Message to record the action in the log file
    script : string
        Name of the script that run the action.

    """
    # Format of the fullname log
    logDir = "logs/"
    now = datetime.datetime.now()
    nowFormat = now.strftime("%Y-%m-%d %H:%M")

    fullNameLog = logDir + nowFormat + "-" + script + ".csv"

    # If "logs" exists, just update the log
    if os.path.exists(logDir):
        update(info, fullNameLog, nowFormat, mode)
    # If not, create it and then update it
    else:
        os.makedirs(logDir)
        print(logDir + " has been created")
        update(info, fullNameLog, nowFormat, mode)

# -*- coding: utf-8 -*-
from pathlib import Path

import colorama as c
import csv
import datetime
import logging
import os
import shlex
import subprocess

cR = c.Style.RESET_ALL


def createHTML(script, fullNameLog):
    print("Runnning {}createhtml.sh{}...".format(c.Style.BRIGHT, cR))
    htmlFile = fullNameLog.lstrip("logs/").rstrip(".csv") + ".html"
    command = "./createhtml.sh " + fullNameLog.lstrip("logs/") + " " + htmlFile + " " + script
    print(command)
    print(htmlFile)
    print(" An HTML file has been created as a viewer of the CSV file: {}{}{}".format(
        c.Style.BRIGHT, htmlFile, cR)
    )

    subprocess.call(shlex.split(command))


def update(info, script, fullNameLog, dateTime, generateHTML, mode="log"):
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
            datefmt="%d/%m/%Y_%I:%M:%S %p"
        )

        # Updating log
        logging.info(info)
    if mode == "csv":
        with open(fullNameLog, "a") as csvFile:
            row = info["time"], info["item"], info["key"], info["msg"]
            writer = csv.writer(csvFile, lineterminator="\n")
            writer.writerow(row)
    else:
        print("Something goes wrong with the mode of the log")

    if generateHTML is False:
        pass
    elif generateHTML is True:
        createHTML(script, fullNameLog)
    else:
        print("Something goes wrong!")

    return fullNameLog, dateTime


def check(info, script, mode="log", generateHTML=False):
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
    nowFormat = now.strftime("%Y-%m-%d")

    fullNameLog = logDir + nowFormat + "-" + script + ".csv"

    # If "logs" exists, just update the log
    if os.path.exists(logDir):
        pass
    else:
        os.makedirs(logDir)
        print(logDir + " has been created")

    if Path(fullNameLog).is_file():
        update(info, script, fullNameLog, nowFormat, generateHTML, mode)
    # If not, create it and then update it
    else:
        if mode == "csv":
            with open(fullNameLog, "a") as csvFile:
                row = ["timestamp", "item", "subject", "action"]
                writer = csv.writer(csvFile, lineterminator="\n")
                writer.writerow(row)
            update(info, script, fullNameLog, nowFormat, generateHTML, mode)
        else:
            update(info, script, fullNameLog, nowFormat, generateHTML, mode)

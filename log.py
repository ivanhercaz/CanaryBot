# -*- coding: utf-8 -*-
import datetime
import inquirer
import logging
import pywikibot
import os


def update(info, fullNameLog, dateTime):
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
    print("\nUpdating log...")

    # Configuration
    logging.basicConfig(
        filename=fullNameLog,
        level=logging.INFO,
        format=u"%(asctime)s\t%(message)s",
        datefmt="%d/%m/%Y %I:%M:%S %p"
    )

    # Updating log
    logging.info(info)

    return fullNameLog, dateTime


def check(info, script):
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
        update(info, fullNameLog, nowFormat)
    # If not, create it and then update it
    else:
        os.makedirs(logDir)
        print(logDir + " has been created")
        update(info, fullNameLog, nowFormat)

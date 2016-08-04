import requests
import json
import datetime
import dropbox
import os
import shutil

#Your accessToken
accessToken = ""
date = datetime.datetime.now().strftime("%Y-%m-%d")

#The directory where you want to save your backups
backupDir = "backups/"
backupPath = backupDir+date

logfile = backupDir + "log.txt"

#dbx = dropbox.Dropbox(accessToken)
#dbx.users_get_current_account()


def backupFolder(dropboxFolderToBackup):
    files = dbx.files_list_folder(dropboxFolderToBackup, True)

    entries = [] 
    hasMore = files.has_more
    cursor = files.cursor
    
    
    while hasMore:
        files = dbx.files_list_folder_continue(cursor)
        entries += files.entries

        hasMore = files.has_more
        cursor = files.cursor

    for entry in entries:
        saveEntry(entry)


def saveEntry(entry):
    filePath = entry.path_lower
    folder = os.path.split(filePath)[0]
    if not os.path.exists(backupPath + folder):
        os.makedirs(backupPath + folder)
    try:
        dbx.files_download_to_file(backupPath + filePath, filePath)
    except dropbox.exceptions.ApiError as err:        
        logToFile(err)

def removeOldBackups(nrOfBackupsToKeep):
    os.chdir(backupDir)
    backups = os.listdir()
    backups.sort()
    nrOfBackups = len(backups)
    if(nrOfBackups > nrOfBackupsToKeep):
        oldestBackup = backups[0]
        shutil.rmtree(oldestBackup)

def logToFile(error):
    log = open(logfile, "a+")
    log.write(error)
    log.write("\n")
    log.close()

backupFolder("")
removeOldBackups(10)

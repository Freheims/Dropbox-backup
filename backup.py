import requests
import json
import datetime
import dropbox
import os

#Your accessToken
accessToken = ""
date = datetime.datetime.now().strftime("%Y-%m-%d")

#The directory where you want to save your backups
backupDir = "backups/"
backupPath = backupPath+datetime

dbx = dropbox.Dropbox(accessToken)
dbx.users_get_current_account()


def backupFolder(dropboxFolderToBackup):
    os.mkdir(date)
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
    print(folder)
    if not os.path.exists(backupDir + folder):
        os.makedirs(backupDir + folder)
    print(filePath)
    try:
        dbx.files_download_to_file(backupDir + filePath, filePath)
    except dropbox.exceptions.ApiError as err:
        print(filePath)
        print(err)

def main():
    backupFolder("")


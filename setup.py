#!/usr/bin/env python3

import os
import shutil
import helpers


"""
Setup functions, regarding folder structure
"""

def create_folders(pathToFolder):
    """ Creates the folders based on setup """
    try:
        if not os.path.exists(pathToFolder):
            os.makedirs(pathToFolder)
            print("Created folder:", pathToFolder)
        else:
            print("Folder --->", pathToFolder ,"<--- exists. Skipping.")

    except FileNotFoundError:
        print("File not found. Try again.")



def setup_folders(FOLDERS):

    """ Change name on folders """

    for folder in sorted(FOLDERS.keys()):
        if folder not in ("result", "unsorted"):
            ff = helpers.remove_illegal_chars(input("Folder name for " + folder + "? (Enter for default) "))

            if ff is "":
                input("### Leaving " + folder + " folder as default. Press Enter. ###")
            else:
                FOLDERS[folder] = ff

            if folder == "result" or folder == "unsorted":
                create_folders(FOLDERS[folder])
            else:
                create_folders(FOLDERS["result"] + "/" + FOLDERS[folder])

    input("------ Done creating folders. Press any key. -------")


def remove_folder(folder_to_remove):
    """ Deletes result """
    try:
        sure = input("Are you sure you want to delete the folder: '" + folder_to_remove + "'? [y/N] ").lower()
        if sure in ("y", "yes", "Y"):
            shutil.rmtree(folder_to_remove, ignore_errors=False, onerror=None)
        else:
            pass
    except FileNotFoundError:
        print("Folder: '" + folder_to_remove + "' is not created.")

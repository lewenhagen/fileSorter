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
        print("File not found error. Try again.")



def setup_folders(FOLDERS):

    """ Change name on folders """

    for folder in sorted(FOLDERS.keys()):

        ff = helpers.remove_illegal_chars(input("Folder name for " + folder + "? (Enter for default) "))

        if ff is "":
            input("### Leaving " + folder + " folder as default. Press Enter. ###")
        else:
            FOLDERS[folder] = ff

        if folder == "baseFolder" or folder == "unsortedFolder":
            create_folders(FOLDERS[folder])
        else:
            create_folders(FOLDERS["baseFolder"] + "/" + FOLDERS[folder])

    input("------ Done creating folders. Press any key. -------")


def remove_folder(folderToRemove):
    """ Deletes baseFolder """
    try:
        sure = input("Are you sure you want to delete the folder: '" + folderToRemove + "'? [y/N] ").lower()
        if sure in ("y", "yes"):
            shutil.rmtree(folderToRemove, ignore_errors=False, onerror=None)
        else:
            pass
    except FileNotFoundError:
        print("Folder: '" + folderToRemove + "' is not created.")

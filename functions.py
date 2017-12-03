#!/usr/bin/env python3

"""
Functions file
"""

import os
from PIL import Image
import re
# from PythonMagick import Image

# from PIL.ExifTags import TAGS
import imghdr
import magic

from shutil import copy2

MONTHS = {
    "01": "Januari",
    "02": "Februari",
    "03": "Mars",
    "04": "April",
    "05": "Maj",
    "06": "Juni",
    "07": "Juli",
    "08": "Augusti",
    "09": "September",
    "10": "Oktober",
    "11": "November",
    "12": "December",
}

def presentFolders(FOLDERS):

    """ Presents folders to scan """

    sortedFolders = dict()

    for i, x in enumerate(sorted(FOLDERS.keys())):
        sortedFolders[str(i)] = x
        print(str(i) + ")", x)

    while True:
        try:
            scan_me = input("Folder to scan: ")
            scan_folder(FOLDERS, sortedFolders[scan_me])
            break
        except ValueError:
            print("Not a number. Try again.")
        except KeyError:
            print("Number not available. Choose another.")



def scan_folder(FOLDERS, scan_me):

    """ Scans a selected folder, only list # of folders and files """

    nr_of_folders = 0
    nr_of_files = 0
    folderPath = FOLDERS[scan_me]
    structure = []

    if scan_me not in ("result", "unsorted"):
        folderPath = FOLDERS["result"] + "/" + FOLDERS[scan_me]

    for dirname, dirnames, filenames in os.walk(folderPath):
        for subdirname in dirnames:
            structure.append(os.path.join(dirname, subdirname))
            nr_of_folders += 1

        for filename in filenames:
            structure.append(os.path.join(dirname, filename))
            nr_of_files += 1

    print("Folder '" + folderPath + "' contains", str(nr_of_folders), "subfolders and", str(nr_of_files), "files.")

    print_structure = input("View structure? [y/N] ").lower()

    if print_structure in ("y", "yes"):
        os.system("tree " + folderPath)
        # print(*structure, sep="\n")


def get_exif(fn):
    created = {"year": "NA", "month": "NA"}
    try:
        match = re.search("([0-9]*):([0-9]*)", Image.open(fn)._getexif()[306])
        created["year"] = match.group(1)
        created["month"] = MONTHS[match.group(2)]

    except (TypeError, KeyError):
        pass

    return created


def create_structure_and_copy(FOLDERS, images):
    """ Creates the structure from finished images """

    finished_path = FOLDERS["result"] + "/" + FOLDERS["finished"]
    unfinished_path = FOLDERS["result"] + "/" + FOLDERS["unfinished"]

    # print(finished_path) video
    # print(images)
    for image in images:
        create_year = image["created"]["year"]
        create_month = image["created"]["month"]

        # Do the information exist?
        if create_year is not "NA" and create_month is not "NA":
            year_path = finished_path + "/" + create_year
            month_path = year_path + "/" + create_month

            # Create year path folder if not exists
            if not os.path.exists(year_path):
                os.makedirs(year_path)
                print("Created folder:", year_path)

            # Create month path folder if not exists
            if not os.path.exists(month_path):
                os.makedirs(month_path)
                print("Created folder:", month_path)

            copy2(image["image"], month_path)

        else:
            copy2(image["image"], unfinished_path)



def create_structure_and_copy_videos(FOLDERS, videos):
    """ Creates the structure from finished videos """

    finished_path = FOLDERS["result"] + "/" + FOLDERS["finished"] + "/" + FOLDERS["video"]
    unfinished_path = FOLDERS["result"] + "/" + FOLDERS["unfinished"] + "/" + FOLDERS["video"]

    # print(finished_path)

    if not os.path.exists(finished_path):
        os.makedirs(finished_path)
        print("Created folder:", finished_path)

    for video in videos:
        copy2(video["video"], finished_path)



def startSort(FOLDERS):
    """ Initiates the sort """
    images = []
    videos = []
    mime = magic.Magic(mime=True)

    try:
        if not os.listdir(FOLDERS["unsorted"]):
            print("The folder: " + FOLDERS["unsorted"] + " is empty, please dump your photos and videos there.")
        else:
            for dirname, dirnames, filenames in os.walk(FOLDERS["unsorted"]):
                for filename in filenames:
                    if "image" in mime.from_file(os.path.join(dirname, filename)):
                        images.append({
                                "image": os.path.join(dirname, filename),
                                "created": get_exif(os.path.join(dirname, filename))
                            })
                    if "video" in mime.from_file(os.path.join(dirname, filename)):
                        videos.append({
                            "video": os.path.join(dirname, filename),
                            "filename": filename
                        })
            # print(images)
            # print(videos)

            print("------------------ I will now start with the images. ------------------")
            create_structure_and_copy(FOLDERS, images)
            print("------------------ I will now start with the videos. ------------------")
            create_structure_and_copy_videos(FOLDERS, videos)

            # print("HERE:", videos)
    except FileNotFoundError as e:
        print("Error:", e)
        print("I create the folder for you...")
        os.makedirs(FOLDERS["unsorted"])
        print("...done. Folder created.")

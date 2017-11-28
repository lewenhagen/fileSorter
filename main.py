#!/usr/bin/env python3
"""
Main file for program
"""
import parser, sys, setup, functions
import time

FOLDERS = {
    "baseFolder": "Result",
    "finishedFolder": "Finished",
    "unfinishedFolder": "Unfinished",
    "videoFolder": "Video",
    "unsortedFolder": "Unsorted"
}

def main():
    """
    Main function.
    """
    options = parser.parse_options()
    command = options["known_args"]["command"]

    if command == "setup":
        setup.setup_folders(FOLDERS)
    elif command == "clean":
        setup.remove_folder(FOLDERS["baseFolder"])
    elif command == "start":
        start_time = time.time()
        functions.startSort(FOLDERS)
        print("--- %s seconds ---" % (time.time() - start_time))
    elif command == "scan":
        print("\n### Available folders ###\n")
        functions.presentFolders(FOLDERS)
    sys.exit()


if __name__ == "__main__":
    main()

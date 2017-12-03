#!/usr/bin/env python3
"""
Parser file
"""
import argparse

VERSION = "v1.0.0 (2017-10-01)"

options = {}

def parse_options():
    """
    Parse all command line options and arguments and return them as a dictionary.
    """
    parser = argparse.ArgumentParser()
    # group = parser.add_mutually_exclusive_group()
    #
    # group.add_argument("-v", "--verbose", dest="verbose", default="False", help="increase output verbosity", action="store_true")
    # group.add_argument("-s", "--silent", dest="silent", default="False", help="decrease output verbosity", action="store_true")

    parser.add_argument("-V", "--version", action="version", version=VERSION)

    subparsers = parser.add_subparsers(title="commands (positional arguments)", help='Available commands', dest="command")
    subparsers.add_parser("setup", help="Setup the folders needed. Overwrites default.")
    subparsers.add_parser("start", help="Start sorting the files.")
    subparsers.add_parser("clean", help="Removes the result folder.")
    subparsers.add_parser("scan", help="Choose folder to scan.")


    args, unknownargs = parser.parse_known_args()

    options["known_args"] = vars(args)
    options["unknown_args"] = unknownargs

    return options

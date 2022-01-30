#!/usr/bin/env python3
"""Create a pretty-printed JSON file from an Aeon Timeline 2/3 file.

Version @release

usage: extract_json.py [-h] Sourcefile

positional arguments:
  Sourcefile  The path of the .aeonzip or .aeon file.

optional arguments:
  -h, --help  show this help message and exit

Copyright (c) 2021 Peter Triesberger
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import json
import argparse

from pywriter.pywriter_globals import ERROR
from pywaeon2.aeon2_fop import open_timeline
from pywaeon3.aeon3_fop import scan_file

VERSION = 'v@release'
AEON3_EXT = '.aeon'
AEON2_EXT = '.aeonzip'
JSON_EXT = '.json'


def run(sourcePath):
    """Extract JSON data from an .aeonzip or .aeon file
    and create a pretty-printed JSON file.
    Return a message beginning with the ERROR constant in case of error.
    """

    if sourcePath.endswith(AEON3_EXT):
        jsonPart = scan_file(sourcePath)

        if not jsonPart:
            return f'{ERROR}No JSON part found.'

        elif jsonPart.startswith(ERROR):
            return jsonPart

        try:
            jsonData = json.loads(jsonPart)

        except('JSONDecodeError'):
            return f'{ERROR}Invalid JSON data.'

    elif sourcePath.endswith(AEON2_EXT):
        message, jsonData = open_timeline(sourcePath)

        if message.startswith(ERROR):
            return message

    else:
        return(f'{ERROR}File format not supported.')

    targetPath = f'{sourcePath}{JSON_EXT}'

    try:
        with open(targetPath, 'w', encoding='utf-8') as f:
            f.write(json.dumps(jsonData, indent=4, sort_keys=True, ensure_ascii=False))

    except:
        return f'{ERROR}Cannot write "{os.path.normpath(targetPath)}".'

    return f'"{os.path.normpath(targetPath)}" written.'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=f'Create a pretty-printed JSON file from an Aeon Timeline 2/3 file {VERSION}',
        epilog='')
    parser.add_argument('sourcePath', metavar='Sourcefile',
                        help='The path of the .aeonzip or .aeon file.')

    args = parser.parse_args()
    print(run(args.sourcePath))

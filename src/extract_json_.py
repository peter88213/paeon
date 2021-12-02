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

from pywaeon2.aeon2_fop import open_timeline
from paeon.aeon3_fop import scan_file

VERSION = 'v@release'
AEON3_EXT = '.aeon'
AEON2_EXT = '.aeonzip'
JSON_EXT = '.json'


def run(sourcePath):
    """Extract JSON data from an .aeonzip or .aeon file
    and create a pretty-printed JSON file.
    Return a message beginning with SUCCESS or ERROR.
    """

    if sourcePath.endswith(AEON3_EXT):
        jsonPart = scan_file(sourcePath)

        if not jsonPart:
            return 'ERROR: No JSON part found.'

        elif jsonPart.startswith('ERROR'):
            return jsonPart

        try:
            jsonData = json.loads(jsonPart)

        except('JSONDecodeError'):
            return 'ERROR: Invalid JSON data.'

    elif sourcePath.endswith(AEON2_EXT):
        message, jsonData = open_timeline(sourcePath)

        if message.startswith('ERROR'):
            return message

    else:
        return('ERROR: File format not supported.')

    targetPath = sourcePath + JSON_EXT

    try:
        with open(targetPath, 'w', encoding='utf-8') as f:
            f.write(json.dumps(jsonData, indent=4, sort_keys=True, ensure_ascii=False))

    except:
        return 'ERROR: Cannot write "' + os.path.normpath(targetPath) + '".'

    return 'SUCCESS: "' + os.path.normpath(targetPath) + '" written.'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Create a pretty-printed JSON file from an Aeon Timeline 2/3 file ' + VERSION,
        epilog='')
    parser.add_argument('sourcePath', metavar='Sourcefile',
                        help='The path of the .aeonzip or .aeon file.')

    args = parser.parse_args()
    print(run(args.sourcePath))

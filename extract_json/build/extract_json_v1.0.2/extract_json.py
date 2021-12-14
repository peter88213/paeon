#!/usr/bin/env python3
"""Create a pretty-printed JSON file from an Aeon Timeline 2/3 file.

Version 1.0.2

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

import zipfile
import codecs


def open_timeline(filePath):
    """Unzip the project file and read 'timeline.json'.
    Return a message beginning with SUCCESS or ERROR
    and the JSON timeline structure.
    """

    try:
        with zipfile.ZipFile(filePath, 'r') as myzip:
            jsonBytes = myzip.read('timeline.json')
            jsonStr = codecs.decode(jsonBytes, encoding='utf-8')

    except:
        return 'ERROR: Cannot read JSON data.', None

    if not jsonStr:
        return 'ERROR: No JSON part found.', None

    try:
        jsonData = json.loads(jsonStr)

    except('JSONDecodeError'):
        return 'ERROR: Invalid JSON data.'
        None

    return 'SUCCESS', jsonData


def save_timeline(jsonData, filePath):
    """Write the jsonData structure to a zipfile located at filePath.
    Return a message beginning with SUCCESS or ERROR.
    """

    try:

        with zipfile.ZipFile(filePath, 'w') as f:
            f.writestr('timeline.json', json.dumps(jsonData))

    except:
        return 'ERROR: Cannot write JSON data.'

    return 'SUCCESS: "' + os.path.normpath(filePath) + '" written.'


def scan_file(filePath):
    """Read and scan the project file.
    Return a string containing either the JSON part or an error message.
    """

    try:
        with open(filePath, 'rb') as f:
            binInput = f.read()

    except(FileNotFoundError):
        return 'ERROR: "' + os.path.normpath(filePath) + '" not found.'

    except:
        return 'ERROR: Cannot read "' + os.path.normpath(filePath) + '".'

    # JSON part: all characters between the first and last curly bracket.

    chrData = []
    opening = ord('{')
    closing = ord('}')
    level = 0

    for c in binInput:

        if c == opening:
            level += 1

        if level > 0:
            chrData.append(c)

            if c == closing:
                level -= 1

                if level == 0:
                    break

    if level != 0:
        return 'ERROR: Corrupted data.'

    try:
        jsonStr = codecs.decode(bytes(chrData), encoding='utf-8')

    except:
        return 'ERROR: Cannot decode "' + os.path.normpath(filePath) + '".'

    return jsonStr

VERSION = 'v1.0.2'
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

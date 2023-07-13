#!/usr/bin/python3
"""Create a pretty-printed JSON file from an Aeon Timeline 2/3 file.

Version 1.0.6
Requires Python 3.6+

usage: extract_json.py [-h] Sourcefile

positional arguments:
  Sourcefile  The path of the .aeonzip or .aeon file.

optional arguments:
  -h, --help  show this help message and exit

Copyright (c) 2022 Peter Triesberger
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import zipfile
import codecs
import json
import argparse

VERSION = 'v1.0.6'
AEON3_EXT = '.aeon'
AEON2_EXT = '.aeonzip'
JSON_EXT = '.json'
ERROR = 'Error: '


def open_timeline(filePath):
    """Unzip an Aeon Timeline 2 '.aeonzip' project file and read 'timeline.json'.

    Positional arguments:
        filePath -- Path of the .aeon project file to read.
        
    Return a message beginning with the ERROR constant in case of error
    and a Python object containing the timeline structure.
    """
    try:
        with zipfile.ZipFile(filePath, 'r') as myzip:
            jsonBytes = myzip.read('timeline.json')
            jsonStr = codecs.decode(jsonBytes, encoding='utf-8')
    except:
        return f'{ERROR}Cannot read timeline data.', None
    if not jsonStr:
        return f'{ERROR}No JSON part found in timeline data.', None
    try:
        jsonData = json.loads(jsonStr)
    except('JSONDecodeError'):
        return f'{ERROR}Invalid JSON data in timeline.'
        None
    return 'Timeline data read in.', jsonData


def scan_file(filePath):
    """Read and scan an Aeon Timeline 3 '.aeon' project file.
    
    Positional arguments:
        filePath -- str: Path to the Aeon 3 project file.
    
    Return a string containing either the JSON part or an error message.
    """
    try:
        with open(filePath, 'rb') as f:
            binInput = f.read()
    except(FileNotFoundError):
        return f'{ERROR}"{os.path.normpath(filePath)}" not found.'

    except:
        return f'{ERROR}Cannot read "{os.path.normpath(filePath)}".'

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
        return f'{ERROR}Corrupted data.'

    try:
        jsonStr = codecs.decode(bytes(chrData), encoding='utf-8')
    except:
        return f'{ERROR}Cannot decode "{os.path.normpath(filePath)}".'

    return jsonStr


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

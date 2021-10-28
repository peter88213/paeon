#!/usr/bin/env python3
"""Extract the JSON part from an .aeon file
input file : command line parameter
output file : name of the input file with '.json' appended.
"""
import os
import json
import argparse

from paeon.aeon3_fop import scan_file


def run(filePath):
    jsonPart = scan_file(filePath)

    if not jsonPart:
        return 'ERROR: No JSON part found.'

    elif jsonPart.startswith('ERROR'):
        return jsonPart

    try:
        jsonData = json.loads(jsonPart)

    except('JSONDecodeError'):
        return 'ERROR: Invalid JSON data.'

    with open(filePath + '.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(jsonData, indent=4, sort_keys=True))

    return 'SUCCESS: "' + os.path.normpath(filePath) + '.json" written.'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Extract the JSON part from an Aeon Timeline 3 file',
        epilog='')
    parser.add_argument('sourcePath', metavar='Sourcefile',
                        help='The path of the .aeon file.')

    args = parser.parse_args()
    print(run(args.sourcePath))

"""Aeon2 file operation

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/paeon
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import zipfile
import codecs
import json


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
        with zipfile.ZipFile(filePath, 'w', encoding='utf-8', compress_type=zipfile.ZIP_DEFLATED) as f:
            f.writestr('timeline.json', json.dumps(jsonData))

    except:
        return 'ERROR: Cannot write JSON data.'

    return 'SUCCESS'

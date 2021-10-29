"""Aeon2 file operation

Part of the paeon project (https://github.com/peter88213/paeon)
Copyright (c) 2021 Peter Triesberger
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import zipfile
import codecs


def extract_timeline(filePath):
    """Unzip the project file and read 'timeline.json'.
    Return a string containing either the JSON string or an error message.
    """

    try:
        with zipfile.ZipFile(filePath, 'r') as myzip:
            jsonBytes = myzip.read('timeline.json')
            jsonStr = codecs.decode(jsonBytes, encoding='utf-8')

    except:
        return 'ERROR: Cannot read JSON data.'

    return jsonStr

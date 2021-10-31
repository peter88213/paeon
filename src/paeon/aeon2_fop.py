"""Aeon2 file operation

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/paeon
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

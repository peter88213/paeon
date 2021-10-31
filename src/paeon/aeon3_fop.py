"""Aeon3 file operation

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/paeon
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import codecs


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
    chrList = []
    inStr = False
    opening = ord('{')
    closing = ord('}')

    for c in binInput:

        if c == opening:
            inStr = True

        if inStr:
            chrData.append(c)

            if c == closing:
                chrList.extend(chrData)
                chrData = []
    try:
        jsonStr = codecs.decode(bytes(chrList), encoding='utf-8')

    except:
        return 'ERROR: Cannot decode "' + os.path.normpath(filePath) + '".'

    return jsonStr

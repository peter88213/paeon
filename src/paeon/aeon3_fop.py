"""Aeon3 file operation

Part of the paeon project (https://github.com/peter88213/paeon)
Copyright (c) 2021 Peter Triesberger
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os

def scan_file(filePath):
    """Read and scan the project file.
    Return a string containing the JSON part.
    """

    try:
        with open(filePath, 'rb') as f:
            binData = f.read()

    except(FileNotFoundError):
        return 'ERROR: "' + os.path.normpath(filePath) + '" not found.'

    except:
        return 'ERROR: Cannot read "' + os.path.normpath(filePath) + '".'

    # JSON part: all characters between the first and last curly bracket.

    strData = []
    jsonData = []
    inStr = False
    opening = ord('{')
    closing = ord('}')

    for c in binData:

        if c == opening:
            inStr = True

        if inStr:
            strData.append(chr(c))

            if c == closing:
                jsonData.append(('').join(strData))
                strData = []

    return ('').join(jsonData)



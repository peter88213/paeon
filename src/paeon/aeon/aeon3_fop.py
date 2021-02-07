"""Aeon3 file operation

Copyright (c) 2021 Peter Triesberger
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""


def read_aeon3(filePath):
    """Read the Aeon3 project file and separate the JSON part 
    from the "binary" prefix and suffix.

    Call parameter is a string
    filePath: path to an .aeon file

    The .aeon file is read as a text file; the "binary" parts contain non-printable
    characters that could not be decoded as utf-8. So there is no "encoding" 
    specified as open() argument.

    The JSON part begins with the first curly bracket and ends with the last curly bracket.

    Normal operation:
    Return a tuple of four strings
    message beginning with 'SUCCESS', binPrefix, jsonPart, binSuffix

    Error handling:
    Return a tuple of four elements
    message beginning with 'ERROR', None, None, None

    Usage example:

    message, part1, part2, part3 = read_aeon3(pathToAeonProject)

    if message.startswith('ERROR'):
        print(message)
        exit(1)

    process_json_part(part2) 
    """

    try:
        # Read the file as raw string

        with open(filePath, 'r') as f:
            data = f.read()

    except:
        return 'ERROR: Cannot read "' + filePath + '".', None, None, None

    try:

        # Binary prefix: all characters before the first curly bracket

        binPrefix, data = data.split('{', 1)

        # Binary suffix: all characters after the last curly bracket

        data, binSuffix = data.rsplit('}', 1)

        # JSON part: the rest

        jsonPart = '{' + data + '}'

    except:
        return 'ERROR: No JSON part found.', None, None, None

    # Convert the raw JSON part to an utf-8 string

    with open('temp.json', 'w') as f:
        f.write(jsonPart)

    with open('temp.json', 'r', encoding='utf-8') as f:
        jsonPart = f.read()

    return 'SUCCESS: "' + filePath + '" read.', binPrefix, jsonPart, binSuffix


def write_aeon3(filePath, binPrefix, jsonPart, binSuffix):
    """Assemble the Aeon 3 project and write the file.
    Return a message beginning with SUCCESS or ERROR.

    Normal operation:
    Write project data to a text file located at filePath
    Return a message beginning with SUCCESS

    Error handling:
    Return a  message beginning with ERROR

    Usage example:

    print(write_aeon3(pathToAeonProject, part1, part2, part3))
    """

    try:
        # Convert the utf-8 JSON part to a raw string

        with open('temp.json', 'w', encoding='utf-8') as f:
            f.write(jsonPart)

        with open('temp.json', 'r') as f:
            jsonPart = f.read()

        data = binPrefix + jsonPart + binSuffix

    except:
        return 'ERROR: Cannot assemble the project.'

    try:
        with open(filePath, 'w') as f:
            f.write(data)

    except:
        return 'ERROR: Can not write "' + filePath + '".'

    return 'SUCCESS: "' + filePath + '" written.'

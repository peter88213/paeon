"""Aeon3 file operation

Copyright (c) 2021 Peter Triesberger
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""


def split_aeon3(aeonPath, prefixPath, jsonPath, suffixPath):
    """Read the Aeon3 project file and separate the JSON part 
    from the "binary" prefix and suffix.

    The JSON part begins with the first curly bracket and ends with the last curly bracket.

    Parameters
    str aeonPath: Path to the .aeon project file to be read.
    str prefixPath: Path to the binary prefix file to be created.  
    str jsonPath: Path to the JSON file to be created.
    str suffixPath: Path to the  binary suffixfile to be created.

    Return a message beginning with 'SUCCESS' or 'ERROR'.
    """

    try:
        # Read the file as raw string.
        # Note: The .aeon file is read as a text file; the "binary"
        # parts contain non-printable characters that could not be
        # decoded as utf-8. So there is no encoding specified.

        with open(aeonPath, 'r') as f:
            data = f.read()

    except:
        return 'ERROR: Cannot read "' + aeonPath + '".'

    try:
        # Binary prefix: all characters before the first curly bracket

        binPrefix, data = data.split('{', 1)

        # Binary suffix: all characters after the last curly bracket

        data, binSuffix = data.rsplit('}', 1)

        # JSON part: the rest

        jsonPart = '{' + data + '}'

    except:
        return 'ERROR: No JSON part found.'

    # Write split files.

    try:

        with open(prefixPath, 'w') as f:
            f.write(binPrefix)

        with open(jsonPath, 'w') as f:
            f.write(jsonPart)

        with open(suffixPath, 'w') as f:
            f.write(binSuffix)

    except:
        return 'ERROR: Cannot write split files.'

    return 'SUCCESS: Split files written.'


def join_aeon3(aeonPath, prefixPath, jsonPath, suffixPath):
    """Assemble the Aeon 3 project and write the file.

    Parameters
    str aeonPath: Path to the .aeon project file to be created.
    str prefixPath: Path to the binary prefix file to be read.  
    str jsonPath: Path to the JSON file to be read.
    str suffixPath: Path to the binary suffix file to be read.

    Return a message beginning with 'SUCCESS' or 'ERROR'.
    """

    try:
        # Convert the utf-8 JSON part to a raw string

        with open(prefixPath, 'r') as f:
            binPrefix = f.read()

        with open(jsonPath, 'r') as f:
            jsonPart = f.read()

        with open(suffixPath, 'r') as f:
            binSuffix = f.read()

    except:
        return 'ERROR: Cannot read split files.'

    try:
        data = binPrefix + jsonPart + binSuffix

    except:
        return 'ERROR: Cannot assemble the project.'

    try:
        with open(aeonPath, 'w') as f:
            f.write(data)

    except:
        return 'ERROR: Can not write "' + aeonPath + '".'

    return 'SUCCESS: "' + aeonPath + '" written.'

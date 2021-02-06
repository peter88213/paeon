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

    Return a tuple of three strings
    binPrefix, jsonPart, binSuffix: "binary" prefix and suffix, JSON part

    Error handling:

    Return a tuple of three elements
    None, error message, None

    Usage example:

    part1, part2, part3 = read_aeon3(pathToAeonProject)

    if part1 is None:
            print(part2) # Error message
            exit(1)

    process_json_part(part2) 
    """

    try:
        with open(filePath, 'r') as f:
            data = f.read()

    except:
        return None, 'ERROR: Can not read "' + filePath + '".', None

    try:

        # Binary prefix: all characters before the first curly bracket

        binPrefix, data = data.split('{', 1)

        # Binary suffix: all characters after the last curly bracket

        data, binSuffix = data.rsplit('}', 1)

        # JSON part: the rest

        jsonPart = '{' + data + '}'

    except:
        return None, None, 'ERROR: No JSON part found.'

    return binPrefix, jsonPart, binSuffix

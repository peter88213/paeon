"""Aeon3 project file handling

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/paeon
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import sys

from paeon.model.timeline import Timeline
from paeon.aeon.aeon3_fop import read_aeon3, write_aeon3


class Aeon3File(Timeline):
    """Aeon 3 project file representation
    """
    DESCRIPTION = 'Aeon Timeline 3 project file'
    EXTENSION = 'aeon'

    def __init__(self, filePath):
        self.filePath = filePath
        self.binPrefix = ''
        self.binSuffix = ''
        self.jsonPart = ''

    def read(self):
        """Read the Aeon3 project file and separate the JSON part 
        from the binary prefix and suffix.
        Return a message beginning with SUCCESS or ERROR.
        """
        message, self.binPrefix, self.jsonPart, self.binSuffix = read_aeon3(
            self.filePath)
        return message

    def write(self):
        """Assemble the Aeon 3 project and write the file.
        Return a message beginning with SUCCESS or ERROR.
        """

        # Write back the timeline attributes to the JSON part (to come)

        # Assemble binary and JSON parts and write the project file.

        return write_aeon3(self.filePath, self.binPrefix, self.jsonPart, self.binSuffix)

    def write_json(self):
        """Create a JSON file with the Aeon 3 project content.
        Return a message beginning with SUCCESS or ERROR.
        """
        jsonPath = self.filePath.replace(self.EXTENSION, 'json')

        try:
            with open(jsonPath, 'w', encoding='utf-8') as f:
                f.write(self.jsonPart)

        except:
            return 'ERROR: Can not write "' + jsonPath + '".'

        return 'SUCCESS: "' + jsonPath + '" written.'


if __name__ == '__main__':
    project = Aeon3File(sys.argv[1])
    print(project.read())
    print(project.write_json())
    print(project.write())
    text = project.jsonPart.split('"')
    for word in text:
        if "Ä" in word:
            print(word)

"""Aeon3 project file handling

Part of the paeon project (https://github.com/peter88213/paeon)
Copyright (c) 2021 Peter Triesberger
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import sys

from paeon.model.timeline import Timeline
from paeon.aeon.aeon3_fop import split_aeon3, join_aeon3


class Aeon3File(Timeline):
    """Aeon 3 project file representation
    """
    DESCRIPTION = 'Aeon Timeline 3 project file'
    EXTENSION = 'aeon'

    def __init__(self, filePath):
        self.filePath = filePath
        self.jsonPart = ''

    def read(self):
        """Read the timeline attributes from an Aeon3 project file.
        Return a message beginning with SUCCESS or ERROR.
        """

        # Split the project file into binary and JSON parts.

        prefixPath = self.filePath.replace('.' + self.EXTENSION, '.bin1')
        jsonPath = self.filePath.replace('.' + self.EXTENSION, '.json')
        suffixPath = self.filePath.replace('.' + self.EXTENSION, '.bin2')

        message = split_aeon3(self.filePath, prefixPath, jsonPath, suffixPath)

        if message.startswith('ERROR'):
            return message

        # Read the JSON file.

        try:
            with open(jsonPath, 'r', encoding='utf-8') as f:
                self.jsonPart = f.read()

        except:
            return 'ERROR: Cannot read the JSON file.'

        # Parse the JSON part (to come)

        return 'SUCCESS: Project data read.'

    def write(self):
        """Write the timeline attributes to an Aeon3 project file.
        Return a message beginning with SUCCESS or ERROR.
        """

        # Write the timeline attributes to the JSON tree (to come)

        prefixPath = self.filePath.replace('.' + self.EXTENSION, '.bin1')
        jsonPath = self.filePath.replace('.' + self.EXTENSION, '.json')
        suffixPath = self.filePath.replace('.' + self.EXTENSION, '.bin2')

        # Write the JSON file.

        try:

            with open(jsonPath, 'w', encoding='utf-8') as f:
                f.write(self.jsonPart)

        except:
            return 'ERROR: Cannot write the JSON file.'

        # Assemble binary and JSON parts and write the project file.

        return join_aeon3(self.filePath, prefixPath, jsonPath, suffixPath)


if __name__ == '__main__':
    project = Aeon3File(sys.argv[1])
    print(project.read())
    print(project.write())
    text = project.jsonPart.split('"')
    for word in text:
        if "Ä" in word:
            print(word)

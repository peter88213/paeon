"""Aeon3 project file handling

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/paeon
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import sys

from paeon.model.timeline import Timeline


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
        """

        with open(self.filePath, 'r') as f:
            data = f.read()

        # Binary prefix: all characters before the first curly bracket

        self.binPrefix, data = data.split('{', 1)

        # Binary suffix: all characters after the last curly bracket

        data, self.binSuffix = data.rsplit('}', 1)

        # JSON part: the rest

        self.jsonPart = '{' + data + '}'

        # Parse the JSON part (to come)

    def write(self):
        """Assemble the Aeon 3 project and write the file.
        """

        # Write back the timeline attributes to the JSON part (to come)

        # Assemble binary and JSON parts and write the project file.

        data = self.binPrefix + self.jsonPart + self.binSuffix

        with open(self.filePath, 'w') as f:
            f.write(data)

    def write_json(self):
        """Create a JSON file with the Aeon 3 project content.
        """

        with open(self.filePath.replace(self.EXTENSION, 'json'), 'w', encoding='utf-8') as f:
            f.write(self.jsonPart)


if __name__ == '__main__':
    project = Aeon3File(sys.argv[1])
    project.read()
    project.write_json()
    project.write()

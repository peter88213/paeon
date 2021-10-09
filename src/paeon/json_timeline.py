"""Provide a class for Aeon Timeline 3 JSON representation.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/aeon3yw
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import json
from paeon.aeon_timeline import AeonTimeline
from paeon.aeon3_fop import scan_file


class JsonTimeline(AeonTimeline):
    """File representation of an Aeon Timeline 3 project. 

    Represents the JSON part of the project file.
    """

    EXTENSION = '.aeon'
    DESCRIPTION = 'Aeon Timeline 3 project'
    SUFFIX = ''

    def read(self):
        """Extract the JSON part of the Aeon Timeline 3 file located at filePath, 
        fetching the relevant data.
        Extend the superclass.

        Return a message beginning with SUCCESS or ERROR.
        """

        jsonPart = scan_file(self.filePath)

        if not jsonPart:
            return 'ERROR: No JSON part found.'

        elif jsonPart.startswith('ERROR'):
            return jsonPart

        reader = json.loads(jsonPart)

        for label in reader.fieldnames:
            self.labels.append(label)

        for row in reader:
            aeonEntity = {}

            for label in row:
                aeonEntity[label] = row[label]

            self.entities.append(aeonEntity)

        return AeonTimeline.read(self)

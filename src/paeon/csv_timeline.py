"""Provide a class for Aeon Timeline 3 csv representation.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/aeon3yw
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import csv
from paeon.aeon_timeline import AeonTimeline


class CsvTimeline(AeonTimeline):
    """File representation of a csv file exported by Aeon Timeline 3. 

    Represents a csv file with a record per scene.
    - Records are separated by line breaks.
    - Data fields are delimited by commas.
    """

    EXTENSION = '.csv'
    DESCRIPTION = 'Aeon Timeline CSV export'
    SUFFIX = ''

    _SEPARATOR = ','

    def __init__(self, filePath, **kwargs):
        AeonTimeline.__init__(self, filePath, **kwargs)

    def read(self):
        """Parse the csv file located at filePath, fetching the relevant data.
        Extend the superclass.

        Return a message beginning with SUCCESS or ERROR.
        """

        #--- Read the csv file.

        try:
            with open(self.filePath, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter=self._SEPARATOR)

                for label in reader.fieldnames:
                    self.labels.append(label)

                for row in reader:
                    aeonEntity = {}

                    for label in row:
                        aeonEntity[label] = row[label]

                    self.entities.append(aeonEntity)

        except(FileNotFoundError):
            return 'ERROR: "' + os.path.normpath(self.filePath) + '" not found.'

        except:
            return 'ERROR: Can not parse csv file "' + os.path.normpath(self.filePath) + '".'

        return AeonTimeline.read(self)

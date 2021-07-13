"""Provide a class for csv timeline representation.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/paeon
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os

from pywriter.csv.csv_file import CsvFile
from pywriter.model.scene import Scene
from pywriter.model.chapter import Chapter


class CsvTimeline(CsvFile):
    """csv file representation of an Aeon2 time line. 

    Represents a csv file with a record per scene.
    - Records are separated by line breaks.
    - Data fields are delimited by the _SEPARATOR character.
    """

    DESCRIPTION = 'Timeline'
    SUFFIX = ''
    _SEPARATOR = ','

    fileHeader = '''"EventID","Title","Start Date",''' +\
        '''"Duration","End Date","Parent","Color",''' +\
        '''"Tags","Links","Tension","Complete","Summary"''' +\
        ''',"Arc","Location","Observer","Participant"
'''

    sceneTemplate = '''"$ID","$Title","$Date $Time"''' +\
        '''"Duration","End Date","Parent","Color",''' +\
        '''"Tags","Links","Tension","Complete","Summary"''' +\
        ''',"Arc","Location","Observer","Participant"
'''

    def get_sceneMapping(self, scId, sceneNumber, wordsTotal, lettersTotal):
        """Return a mapping dictionary for a scene section. 
        """
        sceneMapping = CsvFile.get_sceneMapping(
            self, scId, sceneNumber, wordsTotal, lettersTotal)

        return sceneMapping

    def read(self):
        """Parse the csv file located at filePath, 
        fetching the Scene attributes contained.
        Return a message beginning with SUCCESS or ERROR.
        """
        message = CsvFile.read(self)

        if message.startswith('ERROR'):
            return message

        self.chapters['1'] = Chapter()
        self.chapters['1'].title = 'Chapter 1'
        self.srtChapters = ['1']

        for cells in self.rows:

            if not cells[0] == 'EventID':
                i = 0

                # Event ID --> scene ID.

                scId = cells[i]
                self.scenes[scId] = Scene()
                i += 1

                # Event title --> scene title.

                self.scenes[scId].title = cells[i]
                i += 1

                # Date and time:

                dt = cells[i].split(' ')
                self.scenes[scId].date = dt[0]
                self.scenes[scId].time = dt[1]
                i += 1
                i += 1
                i += 1
                i += 1
                i += 1
                i += 1
                i += 1
                i += 1
                i += 1

                # Summary --> scene description.

                self.scenes[scId].desc = self.convert_to_yw(cells[i])
                i += 1

                # Arcs --> tags:

                self.scenes[scId].tags = cells[i].split('|')

                self.scenes[scId].status = 1

                self.chapters['1'].srtScenes.append(scId)

        # TODO: sort self.chapters['1'].srtScenes by date/time

        return 'SUCCESS: Data read from "' + os.path.normpath(self.filePath) + '".'

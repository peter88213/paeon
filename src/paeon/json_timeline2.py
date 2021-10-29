"""Provide a class for Aeon Timeline 2 JSON representation.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/aeon3yw
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import sys
import json
from datetime import datetime

from pywriter.file.file_export import FileExport
from pywriter.model.scene import Scene
from pywriter.model.chapter import Chapter
from pywriter.model.world_element import WorldElement
from pywriter.model.character import Character

from paeon.dt_helper import fix_iso_dt
from paeon.aeon2_fop import extract_timeline


class JsonTimeline2(FileExport):
    """File representation of an Aeon Timeline 2 project. 

    Represents the JSON part of the project file.
    """

    EXTENSION = '.aeonzip'
    DESCRIPTION = 'Aeon Timeline 2 project'
    SUFFIX = ''

    # Types

    _TYPE_EVENT = 'event'
    _TYPE_CHARACTER = 'defaultPerson'
    _TYPE_NARRATIVE = 'Narrative Folder'

    # Field names

    _LABEL_FIELD = 'Label'
    _TYPE_FIELD = 'Type'
    _SCENE_FIELD = 'Narrative Position'
    _START_DATE_TIME_FIELD = 'Start Date'
    _END_DATE_TIME_FIELD = 'End Date'

    # User defined properties

    _SCENE_MARKER = 'Scene'
    _DESC_MARKER = 'Description'

    # Events assigned to the "narrative" become
    # regular scenes, the others become Notes scenes.

    def read(self):
        """Extract the JSON part of the Aeon Timeline 2 file located at filePath, 
        fetching the relevant data.
        Extend the superclass.

        Return a message beginning with SUCCESS or ERROR.
        """

        jsonPart = extract_timeline(self.filePath)

        if not jsonPart:
            return 'ERROR: No JSON part found.'

        elif jsonPart.startswith('ERROR'):
            return jsonPart

        try:
            jsonData = json.loads(jsonPart)

        except('JSONDecodeError'):
            return 'ERROR: Invalid JSON data.'

        # Make sure there is an "AD" era.

        eras = jsonData['template']['rangeProperties'][0]['calendar']['eras']
        adEra = None

        for era in eras:

            if era['name'] == 'AD':
                adEra = eras.index(era)
                break

        # Get GUID of user defined properties.

        properties = jsonData['template']['properties']
        sceneGuid = None
        descGuid = None

        for property in properties:

            if property['name'] == self._SCENE_MARKER:
                sceneGuid = property['guid']

            elif property['name'] == self._DESC_MARKER:
                descGuid = property['guid']

        itemsById = jsonData['data']['items']['byId']
        events = {}
        characters = {}

        for uid in itemsById:
            row = itemsById[uid]
            aeonEntity = {}

            if row['type'] == 'event':
                labels = ['label', 'summary', 'startDate', 'duration', 'tags']

                for label in labels:
                    aeonEntity[label] = row[label]

                events[row['id']] = aeonEntity

            elif row['type'] == 'defaultPerson':
                labels = ['label', 'summary', 'tags']

                for label in labels:
                    aeonEntity[label] = row[label]

                characters[row['id']] = aeonEntity

        return


if __name__ == '__main__':
    kwargs = {}
    timeline = JsonTimeline2(sys.argv[1])
    timeline.read()

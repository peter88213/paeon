"""Provide a class for Aeon Timeline 3 JSON representation.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/aeon3yw
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import json
from datetime import datetime

from pywriter.file.file_export import FileExport
from pywriter.model.scene import Scene
from pywriter.model.chapter import Chapter
from pywriter.model.world_element import WorldElement
from pywriter.model.character import Character

from paeon.dt_helper import fix_iso_dt
from paeon.aeon3_fop import scan_file


class JsonTimeline(FileExport):
    """File representation of an Aeon Timeline 3 project. 

    Represents the JSON part of the project file.
    """

    EXTENSION = '.aeon'
    DESCRIPTION = 'Aeon Timeline 3 project'
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

    # Narrative position markers

    _PART_MARKER = 'Part'
    _CHAPTER_MARKER = 'Chapter'
    _SCENE_MARKER = 'Scene'

    # Events assigned to the "narrative" become
    # regular scenes, the others become Notes scenes.

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

        try:
            jsonData = json.loads(jsonPart)

        except('JSONDecodeError'):
            return 'ERROR: Invalid JSON data.'

        # Make sure there is an "AD" era.

        eras = jsonData['definitions']['calendar']['eras']
        adEra = None

        for i in range(len(eras)):

            if eras[i]['name'] == 'AD':
                adEra = i
                break

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

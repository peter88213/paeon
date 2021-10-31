"""Provide a class for Aeon Timeline 3 JSON representation.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/paeon
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import sys
import json
from datetime import datetime

from pywriter.file.file_export import FileExport
from pywriter.model.scene import Scene
from pywriter.model.chapter import Chapter
from pywriter.model.world_element import WorldElement
from pywriter.model.character import Character

from paeon.aeon3_fop import scan_file


class JsonTimeline3(FileExport):
    """File representation of an Aeon Timeline 3 project. 

    Represents the JSON part of the project file.
    """

    EXTENSION = '.aeon'
    DESCRIPTION = 'Aeon Timeline 3 project'
    SUFFIX = ''

    # JSON[data][items][byId][<uid>]

    ITEM_DESCRIPTION = 'summary'
    ITEM_START_DATE = 'startDate'
    ITEM_DURATION = 'duration'
    ITEM_LABEL = 'label'
    ITEM_TAGS = 'tags'
    ITEM_TYPE = 'type'
    ITEM_ID = 'id'

    # JSON[definitions][types][byId]

    TYPE_EVENT = 'defaultEvent'
    TYPE_CHARACTER = 'defaultPerson'
    TYPE_LOCATION = 'defaultLocation'
    TYPE_NARRATIVE = 'narrativePart'

    # JSON[definitions][types][byId][<uid>]

    TYPE_LABEL = 'label'

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

        #--- Create characters, locations, and items.

        crIdsByGuid = {}
        lcIdsByGuid = {}
        itIdsByGuid = {}
        characterCount = 0
        locationCount = 0
        itemCount = 0

        for uid in jsonData['data']['items']['byId']:
            dataItem = jsonData['data']['items']['byId'][uid]

            if dataItem[self.ITEM_TYPE] == self.TYPE_CHARACTER:
                characterCount += 1
                crId = str(characterCount)
                crIdsByGuid[uid] = crId
                self.characters[crId] = Character()
                self.characters[crId].title = dataItem[self.ITEM_LABEL]
                self.characters[crId].desc = dataItem[self.ITEM_DESCRIPTION]
                self.srtCharacters.append(crId)

            elif dataItem[self.ITEM_TYPE] == self.TYPE_LOCATION:
                locationCount += 1
                lcId = str(locationCount)
                lcIdsByGuid[uid] = lcId
                self.locations[lcId] = WorldElement()
                self.locations[crId].title = dataItem[self.ITEM_LABEL]
                self.locations[crId].desc = dataItem[self.ITEM_DESCRIPTION]
                self.srtLocations.append(lcId)

            '''
            elif dataItem[self.ITEM_TYPE] == self.TYPE_ITEM:
                itemCount += 1
                itId = str(itemCount)
                itIdsByGuid[uid] = itId
                self.items[itId] = WorldElement()
                self.items[itId].title = dataItem[self.ITEM_LABEL]
                self.items[itId].desc = dataItem[self.ITEM_DESCRIPTION]
                self.srtItems.append(itId)
            '''

        #--- Create scenes.

        eventCount = 0
        scIdsByDate = {}

        for uid in jsonData['data']['items']['byId']:
            dataItem = jsonData['data']['items']['byId'][uid]

            if dataItem[self.ITEM_TYPE] == self.TYPE_EVENT:
                eventCount += 1
                scId = str(eventCount)
                self.scenes[scId] = Scene()
                #self.scenes[scId].isNotesScene = noScene
                self.scenes[scId].title = dataItem[self.ITEM_LABEL]
                self.scenes[scId].desc = dataItem[self.ITEM_DESCRIPTION]
                timestamp = dataItem[self.ITEM_START_DATE]['timestamp']

                if timestamp is None:
                    timestamp = 0

                if not timestamp in scIdsByDate:
                    scIdsByDate[timestamp] = []

                scIdsByDate[timestamp].append(scId)

        #--- Sort scenes by date/time and place them in chapters.

        chIdNarrative = '1'
        chIdBackground = '2'

        self.chapters[chIdNarrative] = Chapter()
        self.chapters[chIdNarrative].title = 'Chapter 1'
        self.chapters[chIdNarrative].chType = 0
        self.srtChapters.append(chIdNarrative)

        self.chapters[chIdBackground] = Chapter()
        self.chapters[chIdBackground].title = 'Background'
        self.chapters[chIdBackground].chType = 1
        self.srtChapters.append(chIdBackground)

        srtScenes = sorted(scIdsByDate.items())

        for date, scList in srtScenes:

            for scId in scList:

                if self.scenes[scId].isNotesScene:
                    self.chapters[chIdBackground].srtScenes.append(scId)

                else:
                    self.chapters[chIdNarrative].srtScenes.append(scId)

        return 'SUCCESS: Data read from "' + os.path.normpath(self.filePath) + '".'

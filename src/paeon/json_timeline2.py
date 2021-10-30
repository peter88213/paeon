"""Provide a class for Aeon Timeline 2 JSON representation.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/aeon3yw
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

from paeon.aeon2_fop import extract_timeline


class JsonTimeline2(FileExport):
    """File representation of an Aeon Timeline 2 project. 

    Represents the JSON part of the project file.
    """

    EXTENSION = '.aeonzip'
    DESCRIPTION = 'Aeon Timeline 2 project'
    SUFFIX = ''

    # JSON[entities]

    ENTITY_TYPE = 'entityType'
    ENTITY_ID = 'guid'
    ENTITY_LABEL = 'name'
    ENTITY_NOTES = 'notes'

    # JSON[events]

    EVENT_TAGS = 'tags'
    EVENT_LABEL = 'title'

    # JSON[template][types][name]

    TYPE_CHARACTER = 'Person'
    TYPE_LOCATION = 'Location'
    TYPE_ITEM = 'Item'

    # JSON[template][properties][name]

    PROPERTY_SCENE = 'Scene'
    PROPERTY_DESC = 'Description'
    VALUE_FALSE = '0'

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

            if era[self.ENTITY_LABEL] == 'AD':
                adEra = eras.index(era)
                break

        # Get GUID of user defined types.

        types = jsonData['template']['types']
        typeCharacter = None
        typeLocation = None
        typeItem = None

        for aeon2Type in types:

            if aeon2Type[self.ENTITY_LABEL] == self.TYPE_CHARACTER:
                typeCharacter = aeon2Type[self.ENTITY_ID]

            elif aeon2Type[self.ENTITY_LABEL] == self.TYPE_LOCATION:
                typeLocation = aeon2Type[self.ENTITY_ID]

            elif aeon2Type[self.ENTITY_LABEL] == self.TYPE_ITEM:
                typeItem = aeon2Type[self.ENTITY_ID]

        # Create characters, locations, and items.

        aeon2Entities = jsonData['entities']
        crIdsByGuid = {}
        lcIdsByGuid = {}
        itIdsByGuid = {}
        characterCount = 0
        locationCount = 0
        itemCount = 0

        for aeon2Entity in aeon2Entities:

            if aeon2Entity[self.ENTITY_TYPE] == typeCharacter:
                characterCount += 1
                crId = str(characterCount)
                crIdsByGuid[aeon2Entity[self.ENTITY_ID]] = crId
                self.characters[crId] = Character()
                self.characters[crId].title = aeon2Entity[self.ENTITY_LABEL]

                if aeon2Entity['notes']:
                    self.characters[crId].notes = aeon2Entity['notes']

                self.srtCharacters.append(crId)

            elif aeon2Entity[self.ENTITY_TYPE] == typeLocation:
                locationCount += 1
                lcId = str(locationCount)
                lcIdsByGuid[aeon2Entity[self.ENTITY_ID]] = lcId
                self.locations[lcId] = WorldElement()
                self.locations[lcId].title = aeon2Entity[self.ENTITY_LABEL]
                self.srtLocations.append(lcId)

            elif aeon2Entity[self.ENTITY_TYPE] == typeItem:
                itemCount += 1
                itId = str(itemCount)
                itIdsByGuid[aeon2Entity[self.ENTITY_ID]] = itId
                self.items[itId] = WorldElement()
                self.items[itId].title = aeon2Entity[self.ENTITY_LABEL]
                self.srtItems.append(itId)

        # Get GUID of user defined properties.

        properties = jsonData['template']['properties']
        propertyScene = None
        propertyDescription = None

        for property in properties:

            if property[self.ENTITY_LABEL] == self.PROPERTY_SCENE:
                propertyScene = property[self.ENTITY_ID]

            elif property[self.ENTITY_LABEL] == self.PROPERTY_DESC:
                propertyDescription = property[self.ENTITY_ID]

        # Create scenes.

        aeon2Events = jsonData['events']
        eventCount = 0
        scIdsByDate = {}

        for aeon2Event in aeon2Events:
            eventCount += 1
            scId = str(eventCount)
            self.scenes[scId] = Scene()
            self.scenes[scId].title = aeon2Event[self.EVENT_LABEL]

            for eventVal in aeon2Event['values']:

                if eventVal['property'] == propertyScene:

                    if eventVal['value'] == self.VALUE_FALSE:
                        self.scenes[scId].isNotesScene = True

                    else:
                        self.scenes[scId].isNotesScene = False

                elif eventVal['property'] == propertyDescription:

                    if eventVal['value']:
                        self.scenes[scId].desc = eventVal['value']

            if aeon2Event[self.EVENT_TAGS]:

                if self.scenes[scId].tags is None:
                    self.scenes[scId].tags = []

                for tag in aeon2Event[self.EVENT_TAGS]:
                    self.scenes[scId].tags.append(tag)

            timestamp = aeon2Event['rangeValues'][0]['position']['timestamp']

            if not timestamp in scIdsByDate:
                scIdsByDate[timestamp] = []

            scIdsByDate[timestamp].append(scId)

        # Sort scenes by date/time and place them in one single chapter.

        chId = '1'
        self.chapters[chId] = Chapter()
        self.chapters[chId].title = 'Chapter 1'
        self.srtChapters = [chId]
        srtScenes = sorted(scIdsByDate.items())

        for date, scList in srtScenes:

            for scId in scList:
                self.chapters[chId].srtScenes.append(scId)

        return 'SUCCESS: Data read from "' + os.path.normpath(self.filePath) + '".'


if __name__ == '__main__':
    kwargs = {}
    timeline = JsonTimeline2(sys.argv[1])
    timeline.read()

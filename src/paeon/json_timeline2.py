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

    # JSON[template][types][name]

    TYPE_CHARACTER = 'Person'
    TYPE_LOCATION = 'Location'
    TYPE_ITEM = 'Item'

    # JSON[template][properties][name]

    PROPERTY_SCENE = 'Scene'
    PROPERTY_DESC = 'Description'

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

        # Get GUID of user defined types.

        types = jsonData['template']['types']
        typeCharacter = None
        typeLocation = None
        typeItem = None

        for aeonType in types:

            if aeonType['name'] == self.TYPE_CHARACTER:
                typeCharacter = aeonType['guid']

            elif aeonType['name'] == self.TYPE_LOCATION:
                typeLocation = aeonType['guid']

            elif aeonType['name'] == self.TYPE_ITEM:
                typeItem = aeonType['guid']

        # Create characters, locations, and items.

        entitiesById = jsonData['entities']
        crIdsByGuid = {}
        lcIdsByGuid = {}
        itIdsByGuid = {}
        characterCount = 0
        locationCount = 0
        itemCount = 0

        labels = ['name', 'notes']

        for entity in entitiesById:

            if entity['entityType'] == typeCharacter:
                characterCount += 1
                crId = str(characterCount)
                crIdsByGuid[entity['guid']] = crId
                self.characters[crId] = Character()
                self.characters[crId].title = entity['name']

                if entity['notes']:
                    self.characters[crId].notes = entity['notes']

                self.srtCharacters.append(crId)

            elif entity['entityType'] == typeLocation:
                locationCount += 1
                lcId = str(locationCount)
                lcIdsByGuid[entity['guid']] = lcId
                self.locations[lcId] = WorldElement()
                self.locations[lcId].title = entity['name']
                self.srtLocations.append(lcId)

            elif entity['entityType'] == typeItem:
                itemCount += 1
                itId = str(itemCount)
                itIdsByGuid[entity['guid']] = itId
                self.items[itId] = WorldElement()
                self.items[itId].title = entity['name']
                self.srtItems.append(itId)

        # Get GUID of user defined properties.

        properties = jsonData['template']['properties']
        propertyScene = None
        propertyDescription = None

        for property in properties:

            if property['name'] == self.PROPERTY_SCENE:
                propertyScene = property['guid']

            elif property['name'] == self.PROPERTY_DESC:
                propertyDescription = property['guid']

        # Create scenes.

        eventsById = jsonData['events']
        eventCount = 0
        scIdsByDate = {}

        for event in eventsById:
            eventCount += 1
            scId = str(eventCount)
            self.scenes[scId] = Scene()
            #self.scenes[scId].isNotesScene = noScene
            self.scenes[scId].title = event['title']
            #self.scenes[scId].desc = event['title']
            timestamp = event['rangeValues'][0]['position']['timestamp']

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

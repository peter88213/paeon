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
    ENTITY_TITLE = 'name'
    ENTITY_NOTES = 'notes'

    # JSON[events]

    EVENT_TAGS = 'tags'
    EVENT_TITLE = 'title'

    # JSON[template][types][name]

    TYPE_CHARACTER = 'Person'
    TYPE_LOCATION = 'Location'
    TYPE_ITEM = 'Item'

    # JSON[template][types][name][roles]

    ROLE_CHARACTER = 'Participant'
    ROLE_LOCATION = 'Location'
    ROLE_ITEM = 'Item'

    # JSON[template][properties][name]

    PROPERTY_SCENE = 'Scene'
    PROPERTY_DESC = 'Description'
    VALUE_TRUE = '1'

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

        #--- Get the "AD" era indicator.

        eras = jsonData['template']['rangeProperties'][0]['calendar']['eras']
        adEra = None

        for era in eras:

            if era['name'] == 'AD':
                adEra = eras.index(era)
                break

        #--- Get GUID of user defined types and roles.

        types = jsonData['template']['types']
        typeCharacter = None
        typeLocation = None
        typeItem = None
        roleCharacter = None
        roleLocation = None
        roleItem = None

        for aeon2Type in types:

            if aeon2Type['name'] == self.TYPE_CHARACTER:
                typeCharacter = aeon2Type['guid']

                for aeon2Role in aeon2Type['roles']:

                    if aeon2Role['name'] == self.ROLE_CHARACTER:
                        roleCharacter = aeon2Role['guid']

            elif aeon2Type['name'] == self.TYPE_LOCATION:
                typeLocation = aeon2Type['guid']

                for aeon2Role in aeon2Type['roles']:

                    if aeon2Role['name'] == self.ROLE_LOCATION:
                        roleLocation = aeon2Role['guid']

            elif aeon2Type['name'] == self.TYPE_ITEM:
                typeItem = aeon2Type['guid']

                for aeon2Role in aeon2Type['roles']:

                    if aeon2Role['name'] == self.ROLE_ITEM:
                        roleItem = aeon2Role['guid']

        #--- Create characters, locations, and items.

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
                crIdsByGuid[aeon2Entity['guid']] = crId
                self.characters[crId] = Character()
                self.characters[crId].title = aeon2Entity[self.ENTITY_TITLE]

                if aeon2Entity['notes']:
                    self.characters[crId].notes = aeon2Entity['notes']

                self.srtCharacters.append(crId)

            elif aeon2Entity[self.ENTITY_TYPE] == typeLocation:
                locationCount += 1
                lcId = str(locationCount)
                lcIdsByGuid[aeon2Entity['guid']] = lcId
                self.locations[lcId] = WorldElement()
                self.locations[lcId].title = aeon2Entity[self.ENTITY_TITLE]
                self.srtLocations.append(lcId)

            elif aeon2Entity[self.ENTITY_TYPE] == typeItem:
                itemCount += 1
                itId = str(itemCount)
                itIdsByGuid[aeon2Entity['guid']] = itId
                self.items[itId] = WorldElement()
                self.items[itId].title = aeon2Entity[self.ENTITY_TITLE]
                self.srtItems.append(itId)

        #--- Get GUID of user defined properties.

        properties = jsonData['template']['properties']
        propertyScene = None
        propertyDescription = None

        for property in properties:

            if property[self.ENTITY_TITLE] == self.PROPERTY_SCENE:
                propertyScene = property['guid']

            elif property[self.ENTITY_TITLE] == self.PROPERTY_DESC:
                propertyDescription = property['guid']

        #--- Create scenes.

        aeon2Events = jsonData['events']
        eventCount = 0
        scIdsByDate = {}

        for aeon2Event in aeon2Events:
            eventCount += 1
            scId = str(eventCount)
            self.scenes[scId] = Scene()
            self.scenes[scId].title = aeon2Event[self.EVENT_TITLE]

            #--- Make non-scene events "Note" type scenes.

            self.scenes[scId].isNotesScene = True

            for eventVal in aeon2Event['values']:

                if eventVal['property'] == propertyScene:

                    if eventVal['value'] == self.VALUE_TRUE:
                        self.scenes[scId].isNotesScene = False

                elif eventVal['property'] == propertyDescription:

                    if eventVal['value']:
                        self.scenes[scId].desc = eventVal['value']

            #--- Get scene tags.

            if aeon2Event[self.EVENT_TAGS]:

                if self.scenes[scId].tags is None:
                    self.scenes[scId].tags = []

                for tag in aeon2Event[self.EVENT_TAGS]:
                    self.scenes[scId].tags.append(tag)

            #--- Get characters, locations, and items.

            for relation in aeon2Event['relationships']:

                if relation['role'] == roleCharacter:

                    if self.scenes[scId].characters is None:
                        self.scenes[scId].characters = []

                    crId = crIdsByGuid[relation['entity']]
                    self.scenes[scId].characters.append(crId)

                elif relation['role'] == roleLocation:

                    if self.scenes[scId].locations is None:
                        self.scenes[scId].locations = []

                    lcId = lcIdsByGuid[relation['entity']]
                    self.scenes[scId].locations.append(lcId)

                elif relation['role'] == roleItem:

                    if self.scenes[scId].items is None:
                        self.scenes[scId].items = []

                    itId = itIdsByGuid[relation['entity']]
                    self.scenes[scId].items.append(itId)

            #--- Get the timestamp for chronological sorting.

            timestamp = aeon2Event['rangeValues'][0]['position']['timestamp']

            if not timestamp in scIdsByDate:
                scIdsByDate[timestamp] = []

            scIdsByDate[timestamp].append(scId)

            #--- Get date/time

            #--- Get scene duration.

            span = aeon2Event['rangeValues'][0]['span']
            lastsDays = 0
            lastsHours = 0
            lastsMinutes = 0

            if 'days' in span:
                lastsDays = span['days']

            if 'hours' in span:
                lastsHours = span['hours'] % 24
                lastsDays += span['hours'] // 24

            if 'minutes' in span:
                lastsMinutes = span['minutes'] % 60
                lastsHours += span['minutes'] // 60

            if 'seconds' in span:
                lastsMinutes += span['seconds'] // 60

            lastsHours += lastsMinutes // 60
            lastsMinutes %= 60
            lastsDays += lastsHours // 24
            lastsHours %= 24

            self.scenes[scId].lastsDays = str(lastsDays)
            self.scenes[scId].lastsHours = str(lastsHours)
            self.scenes[scId].lastsMinutes = str(lastsMinutes)

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


if __name__ == '__main__':
    kwargs = {}
    timeline = JsonTimeline2(sys.argv[1])
    timeline.read()

"""Provide a class for Aeon Timeline 2 JSON representation.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/aeon3yw
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import json
from datetime import datetime
from datetime import timedelta

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

    VALUE_TRUE = '1'
    DATE_LIMIT = datetime(100, 1, 1)

    # Events assigned to the "narrative" become
    # regular scenes, the others become Notes scenes.

    def __init__(self, filePath, **kwargs):
        """Extend the superclass constructor,
        defining instance variables.
        """
        FileExport.__init__(self, filePath, **kwargs)

        # JSON[template][properties][name]

        self.propertyScene = kwargs['property_scene']
        self.propertyDesc = kwargs['property_description']
        self.propertyNotes = kwargs['property_notes']

        # JSON[template][types][name][roles]

        self.roleLocation = kwargs['role_location']
        self.roleItem = kwargs['role_item']
        self.roleCharacter = kwargs['role_character']
        self.roleViewpoint = kwargs['role_viewpoint']

        # JSON[template][types][name]

        self.typeCharacter = kwargs['type_character']
        self.typeLocation = kwargs['type_location']
        self.typeItem = kwargs['type_item']

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

        #--- Get the date definition.

        for rp in jsonData['template']['rangeProperties']:

            if rp['type'] == 'date':
                aeonDate = ''
                adEra = None

                for era in rp['calendar']['eras']:

                    if era['name'] == 'AD':
                        adEra = rp['calendar']['eras'].index(era)
                        aeonDate = rp['guid']
                        break

        #--- Get GUID of user defined types and roles.

        types = jsonData['template']['types']
        typeCharacter = None
        typeLocation = None
        typeItem = None
        roleCharacter = None
        roleViewpoint = None
        roleLocation = None
        roleItem = None

        for aeon2Type in types:

            if aeon2Type['name'] == self.typeCharacter:
                typeCharacter = aeon2Type['guid']

                for aeon2Role in aeon2Type['roles']:

                    if aeon2Role['name'] == self.roleCharacter:
                        roleCharacter = aeon2Role['guid']

                    if aeon2Role['name'] == self.roleViewpoint:
                        roleViewpoint = aeon2Role['guid']

            elif aeon2Type['name'] == self.typeLocation:
                typeLocation = aeon2Type['guid']

                for aeon2Role in aeon2Type['roles']:

                    if aeon2Role['name'] == self.roleLocation:
                        roleLocation = aeon2Role['guid']

            elif aeon2Type['name'] == self.typeItem:
                typeItem = aeon2Type['guid']

                for aeon2Role in aeon2Type['roles']:

                    if aeon2Role['name'] == self.roleItem:
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

            if aeon2Entity['entityType'] == typeCharacter:
                characterCount += 1
                crId = str(characterCount)
                crIdsByGuid[aeon2Entity['guid']] = crId
                self.characters[crId] = Character()
                self.characters[crId].title = aeon2Entity['name']

                if aeon2Entity['notes']:
                    self.characters[crId].notes = aeon2Entity['notes']

                self.srtCharacters.append(crId)

            elif aeon2Entity['entityType'] == typeLocation:
                locationCount += 1
                lcId = str(locationCount)
                lcIdsByGuid[aeon2Entity['guid']] = lcId
                self.locations[lcId] = WorldElement()
                self.locations[lcId].title = aeon2Entity['name']
                self.srtLocations.append(lcId)

            elif aeon2Entity['entityType'] == typeItem:
                itemCount += 1
                itId = str(itemCount)
                itIdsByGuid[aeon2Entity['guid']] = itId
                self.items[itId] = WorldElement()
                self.items[itId].title = aeon2Entity['name']
                self.srtItems.append(itId)

        #--- Get GUID of user defined properties.

        properties = jsonData['template']['properties']
        propertyScene = None
        propertyDescription = None
        propertyNotes = None

        for aeon2Property in properties:

            if aeon2Property['name'] == self.propertyScene:
                propertyScene = aeon2Property['guid']

            elif aeon2Property['name'] == self.propertyDesc:
                propertyDescription = aeon2Property['guid']

            elif aeon2Property['name'] == self.propertyNotes:
                propertyNotes = aeon2Property['guid']

        #--- Create scenes.

        aeon2Events = jsonData['events']
        eventCount = 0
        scIdsByDate = {}

        for aeon2Event in aeon2Events:
            eventCount += 1
            scId = str(eventCount)
            self.scenes[scId] = Scene()
            self.scenes[scId].title = aeon2Event['title']

            # Set scene status = "Outline".

            self.scenes[scId].status = 1

            #--- Evaluate properties.

            self.scenes[scId].isNotesScene = True

            for eventVal in aeon2Event['values']:

                # Make scene event "Normal" type scene.

                if eventVal['property'] == propertyScene:

                    if eventVal['value'] == self.VALUE_TRUE:
                        self.scenes[scId].isNotesScene = False

                # Get scene description.

                elif eventVal['property'] == propertyDescription:

                    if eventVal['value']:
                        self.scenes[scId].desc = eventVal['value']

                # Get scene notes.

                elif eventVal['property'] == propertyNotes:

                    if eventVal['value']:
                        self.scenes[scId].sceneNotes = eventVal['value']

            #--- Get scene tags.

            if aeon2Event['tags']:

                if self.scenes[scId].tags is None:
                    self.scenes[scId].tags = []

                for tag in aeon2Event['tags']:
                    self.scenes[scId].tags.append(tag)

            #--- Get characters, locations, and items.

            for rel in aeon2Event['relationships']:

                if rel['role'] == roleCharacter:

                    if self.scenes[scId].characters is None:
                        self.scenes[scId].characters = []

                    crId = crIdsByGuid[rel['entity']]
                    self.scenes[scId].characters.append(crId)

                elif rel['role'] == roleViewpoint:

                    crId = crIdsByGuid[rel['entity']]

                    if self.scenes[scId].characters is None:
                        self.scenes[scId].characters = []

                    elif crId in self.scenes[scId].characters:
                        self.scenes[scId].characters.remove[crId]

                    self.scenes[scId].characters.insert(0, crId)

                elif rel['role'] == roleLocation:

                    if self.scenes[scId].locations is None:
                        self.scenes[scId].locations = []

                    lcId = lcIdsByGuid[rel['entity']]
                    self.scenes[scId].locations.append(lcId)

                elif rel['role'] == roleItem:

                    if self.scenes[scId].items is None:
                        self.scenes[scId].items = []

                    itId = itIdsByGuid[rel['entity']]
                    self.scenes[scId].items.append(itId)

            #--- Get date/time

            timestamp = 0

            for rv in aeon2Event['rangeValues']:

                if rv['rangeProperty'] == aeonDate:
                    timestamp = rv['position']['timestamp']

                    if timestamp > 0:
                        dt = datetime.min + timedelta(seconds=timestamp)

                        if dt >= self.DATE_LIMIT:
                            startDateTime = dt.isoformat().split('T')
                            self.scenes[scId].date = startDateTime[0]
                            self.scenes[scId].time = startDateTime[1]

                #--- Get scene duration.

                lastsDays = 0
                lastsHours = 0
                lastsMinutes = 0

                if 'years' in rv['span']:
                    lastsDays = rv['span']['years'] * 365
                    # Leap years are not taken into account

                if 'days' in rv['span']:
                    lastsDays += rv['span']['days']

                if 'hours' in rv['span']:
                    lastsHours = rv['span']['hours'] % 24
                    lastsDays += rv['span']['hours'] // 24

                if 'minutes' in rv['span']:
                    lastsMinutes = rv['span']['minutes'] % 60
                    lastsHours += rv['span']['minutes'] // 60

                if 'seconds' in rv['span']:
                    lastsMinutes += rv['span']['seconds'] // 60

                lastsHours += lastsMinutes // 60
                lastsMinutes %= 60
                lastsDays += lastsHours // 24
                lastsHours %= 24

                self.scenes[scId].lastsDays = str(lastsDays)
                self.scenes[scId].lastsHours = str(lastsHours)
                self.scenes[scId].lastsMinutes = str(lastsMinutes)

            # Use the timestamp for chronological sorting.

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

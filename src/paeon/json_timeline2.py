"""Provide a class for Aeon Timeline 2 JSON representation.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/paeon
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import json
from datetime import datetime
from datetime import timedelta

from pywriter.model.novel import Novel
from pywriter.model.scene import Scene
from pywriter.model.chapter import Chapter
from pywriter.model.world_element import WorldElement
from pywriter.model.character import Character

from paeon.aeon2_fop import extract_timeline


class JsonTimeline2(Novel):
    """File representation of an Aeon Timeline 2 project. 
    Represents the .aeonzip file containing 'timeline.json'.
    """

    EXTENSION = '.aeonzip'
    DESCRIPTION = 'Aeon Timeline 2 project'
    SUFFIX = ''

    VALUE_TRUE = '1'
    DATE_LIMIT = datetime(100, 1, 1)

    def __init__(self, filePath, **kwargs):
        """Extend the superclass constructor,
        defining instance variables.
        """
        Novel.__init__(self, filePath, **kwargs)

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
        """Read the JSON part of the Aeon Timeline 2 file located at filePath, 
        and build a yWriter novel structure.
        - Events marked as scenes are converted to scenes in one single chapter.
        - Other events are converted to “Notes” scenes in another chapter.
        Return a message beginning with SUCCESS or ERROR.
        Override the superclass method.
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

        for tplRgp in jsonData['template']['rangeProperties']:

            if tplRgp['type'] == 'date':
                aeonDate = ''

                for tplRgpCalEra in tplRgp['calendar']['eras']:

                    if tplRgpCalEra['name'] == 'AD':
                        aeonDate = tplRgp['guid']
                        break

        #--- Get GUID of user defined types and roles.

        typeCharacter = None
        typeLocation = None
        typeItem = None
        roleCharacter = None
        roleViewpoint = None
        roleLocation = None
        roleItem = None

        for tplTyp in jsonData['template']['types']:

            if tplTyp['name'] == self.typeCharacter:
                typeCharacter = tplTyp['guid']

                for tplTypRol in tplTyp['roles']:

                    if tplTypRol['name'] == self.roleCharacter:
                        roleCharacter = tplTypRol['guid']

                    elif tplTypRol['name'] == self.roleViewpoint:
                        roleViewpoint = tplTypRol['guid']

            elif tplTyp['name'] == self.typeLocation:
                typeLocation = tplTyp['guid']

                for tplTypRol in tplTyp['roles']:

                    if tplTypRol['name'] == self.roleLocation:
                        roleLocation = tplTypRol['guid']
                        break

            elif tplTyp['name'] == self.typeItem:
                typeItem = tplTyp['guid']

                for tplTypRol in tplTyp['roles']:

                    if tplTypRol['name'] == self.roleItem:
                        roleItem = tplTypRol['guid']
                        break

        #--- Create characters, locations, and items.

        crIdsByGuid = {}
        lcIdsByGuid = {}
        itIdsByGuid = {}
        characterCount = 0
        locationCount = 0
        itemCount = 0

        for ent in jsonData['entities']:

            if ent['entityType'] == typeCharacter:
                characterCount += 1
                crId = str(characterCount)
                crIdsByGuid[ent['guid']] = crId
                self.characters[crId] = Character()
                self.characters[crId].title = ent['name']

                if ent['notes']:
                    self.characters[crId].notes = ent['notes']

                self.srtCharacters.append(crId)

            elif ent['entityType'] == typeLocation:
                locationCount += 1
                lcId = str(locationCount)
                lcIdsByGuid[ent['guid']] = lcId
                self.locations[lcId] = WorldElement()
                self.locations[lcId].title = ent['name']
                self.srtLocations.append(lcId)

            elif ent['entityType'] == typeItem:
                itemCount += 1
                itId = str(itemCount)
                itIdsByGuid[ent['guid']] = itId
                self.items[itId] = WorldElement()
                self.items[itId].title = ent['name']
                self.srtItems.append(itId)

        #--- Get GUID of user defined properties.

        propertyScene = None
        propertyDescription = None
        propertyNotes = None

        for tplPrp in jsonData['template']['properties']:

            if tplPrp['name'] == self.propertyScene:
                propertyScene = tplPrp['guid']

            elif tplPrp['name'] == self.propertyDesc:
                propertyDescription = tplPrp['guid']

            elif tplPrp['name'] == self.propertyNotes:
                propertyNotes = tplPrp['guid']

        #--- Create scenes.

        eventCount = 0
        scIdsByDate = {}

        for evt in jsonData['events']:
            eventCount += 1
            scId = str(eventCount)
            self.scenes[scId] = Scene()
            self.scenes[scId].title = evt['title']

            # Set scene status = "Outline".

            self.scenes[scId].status = 1

            #--- Evaluate properties.

            self.scenes[scId].isNotesScene = True

            for evtVal in evt['values']:

                # Make scene event "Normal" type scene.

                if evtVal['property'] == propertyScene:

                    if evtVal['value'] == self.VALUE_TRUE:
                        self.scenes[scId].isNotesScene = False

                # Get scene description.

                elif evtVal['property'] == propertyDescription:

                    if evtVal['value']:
                        self.scenes[scId].desc = evtVal['value']

                # Get scene notes.

                elif evtVal['property'] == propertyNotes:

                    if evtVal['value']:
                        self.scenes[scId].sceneNotes = evtVal['value']

            #--- Get scene tags.

            if evt['tags']:

                if self.scenes[scId].tags is None:
                    self.scenes[scId].tags = []

                for evtTag in evt['tags']:
                    self.scenes[scId].tags.append(evtTag)

            #--- Get characters, locations, and items.

            for evtRel in evt['relationships']:

                if evtRel['role'] == roleCharacter:

                    if self.scenes[scId].characters is None:
                        self.scenes[scId].characters = []

                    crId = crIdsByGuid[evtRel['entity']]
                    self.scenes[scId].characters.append(crId)

                elif evtRel['role'] == roleViewpoint:

                    crId = crIdsByGuid[evtRel['entity']]

                    if self.scenes[scId].characters is None:
                        self.scenes[scId].characters = []

                    elif crId in self.scenes[scId].characters:
                        self.scenes[scId].characters.remove[crId]

                    self.scenes[scId].characters.insert(0, crId)

                elif evtRel['role'] == roleLocation:

                    if self.scenes[scId].locations is None:
                        self.scenes[scId].locations = []

                    lcId = lcIdsByGuid[evtRel['entity']]
                    self.scenes[scId].locations.append(lcId)

                elif evtRel['role'] == roleItem:

                    if self.scenes[scId].items is None:
                        self.scenes[scId].items = []

                    itId = itIdsByGuid[evtRel['entity']]
                    self.scenes[scId].items.append(itId)

            #--- Get date/time

            timestamp = 0

            for evtRgv in evt['rangeValues']:

                if evtRgv['rangeProperty'] == aeonDate:
                    timestamp = evtRgv['position']['timestamp']

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

                if 'years' in evtRgv['span']:
                    lastsDays = evtRgv['span']['years'] * 365
                    # Leap years are not taken into account

                if 'days' in evtRgv['span']:
                    lastsDays += evtRgv['span']['days']

                if 'hours' in evtRgv['span']:
                    lastsHours = evtRgv['span']['hours'] % 24
                    lastsDays += evtRgv['span']['hours'] // 24

                if 'minutes' in evtRgv['span']:
                    lastsMinutes = evtRgv['span']['minutes'] % 60
                    lastsHours += evtRgv['span']['minutes'] // 60

                if 'seconds' in evtRgv['span']:
                    lastsMinutes += evtRgv['span']['seconds'] // 60

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

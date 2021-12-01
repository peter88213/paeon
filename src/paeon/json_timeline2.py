"""Provide a class for Aeon Timeline 2 JSON representation.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/paeon
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
from datetime import datetime
from datetime import timedelta

from pywriter.model.novel import Novel
from pywriter.model.scene import Scene
from pywriter.model.chapter import Chapter
from pywriter.model.world_element import WorldElement
from pywriter.model.character import Character

from paeon.aeon2_fop import open_timeline
from paeon.aeon2_fop import save_timeline
from paeon.uid_helper import get_uid


class JsonTimeline2(Novel):
    """File representation of an Aeon Timeline 2 project. 
    Represents the .aeonzip file containing 'timeline.json'.
    """

    EXTENSION = '.aeonzip'
    DESCRIPTION = 'Aeon Timeline 2 project'
    SUFFIX = ''

    VALUE_YES = '1'
    # JSON representation of "yes" in Aeon2 "yes/no" properties

    DATE_LIMIT = (datetime(100, 1, 1) - datetime.min).total_seconds()
    # Dates before 100-01-01 can not be displayed properly in yWriter

    DEFAULT_TIMESTAMP = (datetime.now() - datetime.min).total_seconds()

    def __init__(self, filePath, **kwargs):
        """Extend the superclass constructor,
        defining instance variables.
        """
        Novel.__init__(self, filePath, **kwargs)

        self.jsonData = None

        # JSON[entities][name]

        self.entityNarrative = kwargs['narrative_arc']

        # JSON[template][properties][name]

        self.propertyDesc = kwargs['property_description']
        self.propertyNotes = kwargs['property_notes']

        # JSON[template][types][name][roles]

        self.roleLocation = kwargs['role_location']
        self.roleItem = kwargs['role_item']
        self.roleCharacter = kwargs['role_character']

        # JSON[template][types][name]

        self.typeCharacter = kwargs['type_character']
        self.typeLocation = kwargs['type_location']
        self.typeItem = kwargs['type_item']

        # GUIDs

        self.tplDateGuid = None
        self.typeArcGuid = None
        self.typeCharacterGuid = None
        self.typeLocationGuid = None
        self.typeItemGuid = None
        self.roleArcGuid = None
        self.roleCharacterGuid = None
        self.roleLocationGuid = None
        self.roleItemGuid = None
        self.entityNarrativeGuid = None

        # Miscellaneous

        self.sceneColor = kwargs['color_scene']
        self.eventColor = kwargs['color_event']
        self.timestampMax = 0
        self.displayIdMax = 0.0
        self.colors = {}

    def read(self):
        """Read the JSON part of the Aeon Timeline 2 file located at filePath, 
        and build a yWriter novel structure.
        - Events marked as scenes are converted to scenes in one single chapter.
        - Other events are converted to “Notes” scenes in another chapter.
        Return a message beginning with SUCCESS or ERROR.
        Override the superclass method.
        """

        message, self.jsonData = open_timeline(self.filePath)

        if message.startswith('ERROR'):
            return message

        #--- Get the color definitions.

        for tplCol in self.jsonData['template']['colors']:
            self.colors[tplCol['name']] = tplCol['guid']

        #--- Get the date definition.

        for tplRgp in self.jsonData['template']['rangeProperties']:

            if tplRgp['type'] == 'date':
                self.tplDateGuid = ''

                for tplRgpCalEra in tplRgp['calendar']['eras']:

                    if tplRgpCalEra['name'] == 'AD':
                        self.tplDateGuid = tplRgp['guid']
                        break

        #--- Get GUID of user defined types and roles.

        for tplTyp in self.jsonData['template']['types']:

            if tplTyp['name'] == 'Arc':
                self.typeArcGuid = tplTyp['guid']

                for tplTypRol in tplTyp['roles']:

                    if tplTypRol['name'] == 'Arc':
                        self.roleArcGuid = tplTypRol['guid']

            elif tplTyp['name'] == self.typeCharacter:
                self.typeCharacterGuid = tplTyp['guid']

                for tplTypRol in tplTyp['roles']:

                    if tplTypRol['name'] == self.roleCharacter:
                        self.roleCharacterGuid = tplTypRol['guid']

            elif tplTyp['name'] == self.typeLocation:
                self.typeLocationGuid = tplTyp['guid']

                for tplTypRol in tplTyp['roles']:

                    if tplTypRol['name'] == self.roleLocation:
                        self.roleLocationGuid = tplTypRol['guid']
                        break

            elif tplTyp['name'] == self.typeItem:
                self.typeItemGuid = tplTyp['guid']

                for tplTypRol in tplTyp['roles']:

                    if tplTypRol['name'] == self.roleItem:
                        self.roleItemGuid = tplTypRol['guid']
                        break

        #--- Create characters, locations, and items.

        crIdsByGuid = {}
        lcIdsByGuid = {}
        itIdsByGuid = {}
        characterCount = 0
        locationCount = 0
        itemCount = 0

        for ent in self.jsonData['entities']:

            if ent['entityType'] == self.typeArcGuid:

                if ent['name'] == self.entityNarrative:
                    self.entityNarrativeGuid = ent['guid']

            elif ent['entityType'] == self.typeCharacterGuid:
                characterCount += 1
                crId = str(characterCount)
                crIdsByGuid[ent['guid']] = crId
                self.characters[crId] = Character()
                self.characters[crId].title = ent['name']

                if ent['notes']:
                    self.characters[crId].notes = ent['notes']

                self.srtCharacters.append(crId)

            elif ent['entityType'] == self.typeLocationGuid:
                locationCount += 1
                lcId = str(locationCount)
                lcIdsByGuid[ent['guid']] = lcId
                self.locations[lcId] = WorldElement()
                self.locations[lcId].title = ent['name']
                self.srtLocations.append(lcId)

            elif ent['entityType'] == self.typeItemGuid:
                itemCount += 1
                itId = str(itemCount)
                itIdsByGuid[ent['guid']] = itId
                self.items[itId] = WorldElement()
                self.items[itId].title = ent['name']
                self.srtItems.append(itId)

        #--- Get GUID of user defined properties.

        propertyDescription = None
        propertyNotes = None

        for tplPrp in self.jsonData['template']['properties']:

            if tplPrp['name'] == self.propertyDesc:
                propertyDescription = tplPrp['guid']

            elif tplPrp['name'] == self.propertyNotes:
                propertyNotes = tplPrp['guid']

        #--- Create scenes.

        eventCount = 0
        scIdsByDate = {}

        for evt in self.jsonData['events']:
            eventCount += 1
            scId = str(eventCount)
            self.scenes[scId] = Scene()
            self.scenes[scId].title = evt['title']

            displayId = float(evt['displayId'])

            if displayId > self.displayIdMax:
                self.displayIdMax = displayId

            # Set scene status = "Outline".

            self.scenes[scId].status = 1

            #--- Evaluate properties.

            for evtVal in evt['values']:

                # Get scene description.

                if evtVal['property'] == propertyDescription:

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

            #--- Get date/time/duration

            timestamp = 0

            for evtRgv in evt['rangeValues']:

                if evtRgv['rangeProperty'] == self.tplDateGuid:
                    timestamp = evtRgv['position']['timestamp']

                    if timestamp >= self.DATE_LIMIT:
                        # Restrict date/time calculation to dates within yWriter's range

                        sceneStart = datetime.min + timedelta(seconds=timestamp)
                        startDateTime = sceneStart.isoformat().split('T')
                        self.scenes[scId].date = startDateTime[0]
                        self.scenes[scId].time = startDateTime[1]

                        # Calculate duration

                        if 'years' in evtRgv['span'] or 'months' in evtRgv['span']:
                            endYear = sceneStart.year
                            endMonth = sceneStart.month

                            if 'years' in evtRgv['span']:
                                endYear += evtRgv['span']['years']

                            if 'months' in evtRgv['span']:
                                endYear += evtRgv['span']['months'] // 12
                                endMonth += evtRgv['span']['months']

                                while endMonth > 12:
                                    endMonth -= 12

                            sceneEnd = datetime(endYear, endMonth, sceneStart.day)
                            sceneDuration = sceneEnd - sceneStart
                            lastsDays = sceneDuration.days
                            lastsHours = sceneDuration.seconds // 3600
                            lastsMinutes = (sceneDuration.seconds % 3600) // 60

                        else:
                            lastsDays = 0
                            lastsHours = 0
                            lastsMinutes = 0

                        if 'weeks' in evtRgv['span']:
                            lastsDays += evtRgv['span']['weeks'] * 7

                        if 'days' in evtRgv['span']:
                            lastsDays += evtRgv['span']['days']

                        if 'hours' in evtRgv['span']:
                            lastsDays += evtRgv['span']['hours'] // 24
                            lastsHours += evtRgv['span']['hours'] % 24

                        if 'minutes' in evtRgv['span']:
                            lastsHours += evtRgv['span']['minutes'] // 60
                            lastsMinutes += evtRgv['span']['minutes'] % 60

                        if 'seconds' in evtRgv['span']:
                            lastsMinutes += evtRgv['span']['seconds'] // 60

                        lastsHours += lastsMinutes // 60
                        lastsMinutes %= 60
                        lastsDays += lastsHours // 24
                        lastsHours %= 24
                        self.scenes[scId].lastsDays = str(lastsDays)
                        self.scenes[scId].lastsHours = str(lastsHours)
                        self.scenes[scId].lastsMinutes = str(lastsMinutes)

                break

            # Use the timestamp for chronological sorting.

            if not timestamp in scIdsByDate:
                scIdsByDate[timestamp] = []

            scIdsByDate[timestamp].append(scId)

            #--- Find scenes and get characters, locations, and items.

            self.scenes[scId].isNotesScene = True
            self.scenes[scId].isUnused = True

            for evtRel in evt['relationships']:

                if evtRel['role'] == self.roleArcGuid:

                    # Make scene event "Normal" type scene.

                    if self.entityNarrativeGuid and evtRel['entity'] == self.entityNarrativeGuid:
                        self.scenes[scId].isNotesScene = False
                        self.scenes[scId].isUnused = False

                        if timestamp > self.timestampMax:
                            self.timestampMax = timestamp

                elif evtRel['role'] == self.roleCharacterGuid:

                    if self.scenes[scId].characters is None:
                        self.scenes[scId].characters = []

                    crId = crIdsByGuid[evtRel['entity']]
                    self.scenes[scId].characters.append(crId)

                elif evtRel['role'] == self.roleLocationGuid:

                    if self.scenes[scId].locations is None:
                        self.scenes[scId].locations = []

                    lcId = lcIdsByGuid[evtRel['entity']]
                    self.scenes[scId].locations.append(lcId)

                elif evtRel['role'] == self.roleItemGuid:

                    if self.scenes[scId].items is None:
                        self.scenes[scId].items = []

                    itId = itIdsByGuid[evtRel['entity']]
                    self.scenes[scId].items.append(itId)

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

    def merge(self, source):
        """Update date/time/duration from the source,
        if the scene title matches.
        """
        message = self.read()

        if message.startswith('ERROR'):
            return message

        # Get scene titles.

        scIdsByTitles = {}
        scIdMax = 0

        for scId in self.scenes:

            if self.scenes[scId].title in scIdsByTitles:
                return 'ERROR: Cannot update because of ambiguous scene titles.'

            else:
                scIdsByTitles[self.scenes[scId].title] = scId

                if int(scId) > scIdMax:
                    scIdMax = int(scId)

        # Get date/time/duration from the source, if the scene title matches.

        for srcId in source.scenes:

            if source.scenes[srcId].title in scIdsByTitles:
                scId = scIdsByTitles[source.scenes[srcId].title]

                if source.scenes[srcId].date or source.scenes[srcId].time:

                    if source.scenes[srcId].date is not None:
                        self.scenes[scId].date = source.scenes[srcId].date

                    if source.scenes[srcId].time is not None:
                        self.scenes[scId].time = source.scenes[srcId].time

                elif source.scenes[srcId].minute or source.scenes[srcId].hour or source.scenes[srcId].day:
                    self.scenes[scId].date = None
                    self.scenes[scId].time = None

                if source.scenes[srcId].minute is not None:
                    self.scenes[scId].minute = source.scenes[srcId].minute

                if source.scenes[srcId].hour is not None:
                    self.scenes[scId].hour = source.scenes[srcId].hour

                if source.scenes[srcId].day is not None:
                    self.scenes[scId].day = source.scenes[srcId].day

                if source.scenes[srcId].lastsMinutes is not None:
                    self.scenes[scId].lastsMinutes = source.scenes[srcId].lastsMinutes

                if source.scenes[srcId].lastsHours is not None:
                    self.scenes[scId].lastsHours = source.scenes[srcId].lastsHours

                if source.scenes[srcId].lastsDays is not None:
                    self.scenes[scId].lastsDays = source.scenes[srcId].lastsDays

            elif source.scenes[srcId].isNotesScene or not source.scenes[srcId].isUnused:
                # Create a new event.

                scIdMax += 1
                newId = str(scIdMax)
                self.scenes[newId] = source.scenes[srcId]

        return 'SUCCESS'

    def write(self):
        """Write selected properties to the file.
        """
        def get_display_id():
            self.displayIdMax += 1
            return str(int(self.displayIdMax))

        def get_timestamp(scene):
            """Return a timestamp integer from the scene date.
            """
            timestamp = int(self.timestampMax)

            try:

                if scene.date:
                    isoDt = scene.date

                    if scene.time:
                        isoDt += (' ' + scene.time)

                timestamp = int((datetime.fromisoformat(isoDt) - datetime.min).total_seconds())

            except:
                pass

            return timestamp

        def get_span(scene):
            """Return a time span dictionary from the scene duration.
            """
            span = {}

            if scene.lastsDays:
                span['days'] = int(scene.lastsDays)

            if scene.lastsHours:
                span['hours'] = int(scene.lastsHours)

            if scene.lastsMinutes:
                span['minutes'] = int(scene.lastsMinutes)

            return span

        def build_event(scene):
            """Convert a scene into an event.
            """
            rangeValue = dict(
                minimumZoom=-1,
                position={
                    'precision': 'minute',
                    'timestamp': get_timestamp(scene)
                },
                rangeProperty=self.tplDateGuid,
                span=get_span(scene),
            )

            relationships = []

            if scene.isNotesScene:
                evColor = self.colors[self.eventColor]

            else:
                narrativeArc = dict(
                    entity=self.entityNarrativeGuid,
                    percentAllocated=1,
                    role=self.roleArcGuid,
                )
                relationships.append(narrativeArc)
                evColor = self.colors[self.sceneColor]

            event = dict(
                attachments=[],
                color=evColor,
                displayId=get_display_id(),
                guid=get_uid(),
                links=[],
                locked=False,
                priority=500,
                rangeValues=[rangeValue],
                relationships=relationships,
                tags=[],
                title=scene.title,
                values=[],
            )
            if scene.tags:
                event['tags'] = scene.tags

            return event

        #--- Create a list of event titles.

        eventTitles = []

        for evt in self.jsonData['events']:
            eventTitles.append(evt['title'])

        #--- Create new events from scenes not listed.

        for scId in self.scenes:

            if not self.scenes[scId].title in eventTitles:
                newEvent = build_event(self.scenes[scId])
                self.jsonData['events'].append(newEvent)

        return save_timeline(self.jsonData, self.filePath)

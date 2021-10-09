"""Provide a class for Aeon Timeline 3 project file representation.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/aeon3yw
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import csv

from datetime import datetime

from pywriter.file.file_export import FileExport
from pywriter.model.scene import Scene
from pywriter.model.chapter import Chapter
from pywriter.model.world_element import WorldElement
from pywriter.model.character import Character

from paeon.dt_helper import fix_iso_dt


class AeonTimeline(FileExport):
    """File representation of a csv file exported by Aeon Timeline 3. 

    Represents a csv file with a record per scene.
    - Records are separated by line breaks.
    - Data fields are delimited by the _SEPARATOR character.
    """

    EXTENSION = '.csv'
    DESCRIPTION = 'Aeon Timeline CSV export'
    SUFFIX = ''

    # Aeon 3 csv export structure (fix part)

    _SCENE_MARKER = 'Scene'
    _CHAPTER_MARKER = 'Chapter'
    _PART_MARKER = 'Part'
    _SCENE_LABEL = 'Narrative Position'
    _TYPE_LABEL = 'Type'
    _EVENT_MARKER = 'Event'
    _STRUCT_MARKER = 'Narrative Folder'
    _START_DATE_TIME_LABEL = 'Start Date'
    _END_DATE_TIME_LABEL = 'End Date'
    _SEPARATOR = ','

    NULL_DATE = '0001-01-01'
    NULL_TIME = '00:00:00'

    # Events assigned to the "varrative" become
    # regular scenes, the others become Notes scenes.

    def __init__(self, filePath, **kwargs):
        """Extend the superclass constructor,
        defining instance variables.
        """
        FileExport.__init__(self, filePath, **kwargs)
        self.partNrPrefix = kwargs['part_number_prefix']

        if self.partNrPrefix:
            self.partNrPrefix += ' '

        self.chapterNrPrefix = kwargs['chapter_number_prefix']

        if self.chapterNrPrefix:
            self.chapterNrPrefix += ' '

        self.partDescLabel = kwargs['part_desc_label']
        self.chapterDescLabel = kwargs['chapter_desc_label']
        self.sceneDescLabel = kwargs['scene_desc_label']
        self.sceneTitleLabel = kwargs['scene_title_label']
        self.notesLabel = kwargs['notes_label']
        self.tagLabel = kwargs['tag_label']
        self.locationLabel = kwargs['location_label']
        self.itemLabel = kwargs['item_label']
        self.characterLabel = kwargs['character_label']
        self.viewpointLabel = kwargs['viewpoint_label']

    def read(self):
        """Parse the csv file located at filePath, 
        fetching the Scene attributes contained.

        Create one single chapter containing all scenes.

        Return a message beginning with SUCCESS or ERROR.
        """
        self.locationCount = 0
        self.locIdsByTitle = {}
        # key = location title
        # value = location ID

        self.itemCount = 0
        self.itmIdsByTitle = {}
        # key = item title
        # value = item ID

        def get_lcIds(lcTitles):
            """Return a list of location IDs; Add new location to the project.
            """
            lcIds = []

            for lcTitle in lcTitles:

                if lcTitle in self.locIdsByTitle:
                    lcIds.append(self.locIdsByTitle[lcTitle])

                elif lcTitle:
                    # Add a new location to the project.

                    self.locationCount += 1
                    lcId = str(self.locationCount)
                    self.locIdsByTitle[lcTitle] = lcId
                    self.locations[lcId] = WorldElement()
                    self.locations[lcId].title = lcTitle
                    self.srtLocations.append(lcId)
                    lcIds.append(lcId)

                else:
                    return None

            return lcIds

        def get_itIds(itTitles):
            """Return a list of item IDs; Add new item to the project.
            """
            itIds = []

            for itTitle in itTitles:

                if itTitle in self.itmIdsByTitle:
                    itIds.append(self.itmIdsByTitle[itTitle])

                elif itTitle:
                    # Add a new item to the project.

                    self.itemCount += 1
                    itId = str(self.itemCount)
                    self.itmIdsByTitle[itTitle] = itId
                    self.items[itId] = WorldElement()
                    self.items[itId].title = itTitle
                    self.srtItems.append(itId)
                    itIds.append(itId)

                else:
                    return None

            return itIds

        self.characterCount = 0
        self.chrIdsByTitle = {}
        # key = character title
        # value = character ID

        def get_crIds(crTitles):
            """Return a list of character IDs; Add new characters to the project.
            """
            crIds = []

            for crTitle in crTitles:

                if crTitle in self.chrIdsByTitle:
                    crIds.append(self.chrIdsByTitle[crTitle])

                elif crTitle:
                    # Add a new character to the project.

                    self.characterCount += 1
                    crId = str(self.characterCount)
                    self.chrIdsByTitle[crTitle] = crId
                    self.characters[crId] = Character()
                    self.characters[crId].title = crTitle
                    self.srtCharacters.append(crId)
                    crIds.append(crId)

                else:
                    return None

            return crIds

        self.rows = []

        #--- Read the csv file.

        try:
            with open(self.filePath, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter=self._SEPARATOR)
                internalDelimiter = ','

                for label in [self._SCENE_LABEL, self.sceneTitleLabel, self._START_DATE_TIME_LABEL, self._END_DATE_TIME_LABEL]:

                    if not label in reader.fieldnames:
                        return 'ERROR: Label "' + label + '" is missing in the CSV file.'

                scIdsByStruc = {}
                chIdsByStruc = {}
                otherEvents = []
                eventCount = 0
                chapterCount = 0

                for row in reader:

                    if row[self._SCENE_LABEL]:
                        narrativeType, narrativePosition = row[self._SCENE_LABEL].split(' ')

                        # Make the narrative position a sortable string.

                        numbers = narrativePosition.split('.')

                        for i in range(len(numbers)):
                            numbers[i] = numbers[i].zfill(4)
                            narrativePosition = ('.').join(numbers)

                    else:
                        narrativeType = ''
                        narrativePosition = ''

                    if row[self._TYPE_LABEL] == self._STRUCT_MARKER:

                        if narrativeType == self._CHAPTER_MARKER:
                            chapterCount += 1
                            chId = str(chapterCount)
                            chIdsByStruc[narrativePosition] = chId
                            self.chapters[chId] = Chapter()
                            self.chapters[chId].chLevel = 0

                            if self.chapterDescLabel:
                                self.chapters[chId].desc = row[self.chapterDescLabel]

                        elif narrativeType == self._PART_MARKER:
                            chapterCount += 1
                            chId = str(chapterCount)
                            chIdsByStruc[narrativePosition] = chId
                            self.chapters[chId] = Chapter()
                            self.chapters[chId].chLevel = 1
                            narrativePosition += '.0000'

                            if self.partDescLabel:
                                self.chapters[chId].desc = row[self.partDescLabel]

                        continue

                    elif row[self._TYPE_LABEL] != self._EVENT_MARKER:
                        continue

                    eventCount += 1
                    scId = str(eventCount)
                    self.scenes[scId] = Scene()

                    if narrativeType == self._SCENE_MARKER:
                        self.scenes[scId].isNotesScene = False
                        scIdsByStruc[narrativePosition] = scId

                    else:
                        self.scenes[scId].isNotesScene = True
                        otherEvents.append(scId)

                    self.scenes[scId].title = row[self.sceneTitleLabel]

                    startDateTimeStr = fix_iso_dt(row[self._START_DATE_TIME_LABEL])

                    if startDateTimeStr is not None:
                        startDateTime = startDateTimeStr.split(' ')
                        self.scenes[scId].date = startDateTime[0]
                        self.scenes[scId].time = startDateTime[1]
                        endDateTimeStr = fix_iso_dt(row[self._END_DATE_TIME_LABEL])

                        if endDateTimeStr is not None:

                            # Calculate duration of scenes that begin after 99-12-31.

                            sceneStart = datetime.fromisoformat(startDateTimeStr)
                            sceneEnd = datetime.fromisoformat(endDateTimeStr)
                            sceneDuration = sceneEnd - sceneStart
                            lastsHours = sceneDuration.seconds // 3600
                            lastsMinutes = (sceneDuration.seconds % 3600) // 60

                            self.scenes[scId].lastsDays = str(sceneDuration.days)
                            self.scenes[scId].lastsHours = str(lastsHours)
                            self.scenes[scId].lastsMinutes = str(lastsMinutes)

                    else:
                        self.scenes[scId].date = self.NULL_DATE
                        self.scenes[scId].time = self.NULL_TIME

                    if self.sceneDescLabel in row:
                        self.scenes[scId].desc = row[self.sceneDescLabel]

                    if self.notesLabel in row:
                        self.scenes[scId].sceneNotes = row[self.notesLabel]

                    if self.tagLabel in row and row[self.tagLabel] != '':
                        self.scenes[scId].tags = row[self.tagLabel].split(internalDelimiter)

                    if self.locationLabel in row:
                        self.scenes[scId].locations = get_lcIds(row[self.locationLabel].split(internalDelimiter))

                    if self.characterLabel in row:
                        self.scenes[scId].characters = get_crIds(row[self.characterLabel].split(internalDelimiter))

                    if self.viewpointLabel in row:
                        vpIds = get_crIds([row[self.viewpointLabel]])

                        if vpIds is not None:
                            vpId = vpIds[0]

                            if self.scenes[scId].characters is None:
                                self.scenes[scId].characters = []

                            elif vpId in self.scenes[scId].characters:
                                self.scenes[scId].characters.remove[vpId]

                            self.scenes[scId].characters.insert(0, vpId)

                    if self.itemLabel in row:
                        self.scenes[scId].items = get_itIds(row[self.itemLabel].split(internalDelimiter))

                    # Set scene status = "Outline".

                    self.scenes[scId].status = 1

        except(FileNotFoundError):
            return 'ERROR: "' + os.path.normpath(self.filePath) + '" not found.'

        except(KeyError):
            return 'ERROR: Wrong csv structure.'

        except(ValueError):
            return 'ERROR: Wrong date/time format.'

        except:
            return 'ERROR: Can not parse "' + os.path.normpath(self.filePath) + '".'

        # Build the chapter structure as defined with Aeon v3.

        srtChpDict = sorted(chIdsByStruc.items())
        srtScnDict = sorted(scIdsByStruc.items())

        partNr = 0
        chapterNr = 0

        for ch in srtChpDict:
            self.srtChapters.append(ch[1])

            if self.chapters[ch[1]].chLevel == 0:
                chapterNr += 1
                self.chapters[ch[1]].title = self.chapterNrPrefix + str(chapterNr)

                for sc in srtScnDict:

                    if sc[0].startswith(ch[0]):
                        self.chapters[ch[1]].srtScenes.append(sc[1])

            else:
                partNr += 1
                self.chapters[ch[1]].title = self.partNrPrefix + str(partNr)

        # Create a chapter for the non-narrative events.

        chapterNr += 1
        chId = str(chapterCount + 1)
        self.chapters[chId] = Chapter()
        self.chapters[chId].title = 'Other events'
        self.chapters[chId].desc = 'Scenes generated from events that ar not assigned to the narrative structure.'
        self.chapters[chId].chType = 1
        self.chapters[chId].srtScenes = otherEvents
        self.srtChapters.append(chId)

        return 'SUCCESS: Data read from "' + os.path.normpath(self.filePath) + '".'

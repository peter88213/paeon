"""Provide a class for Aeon Timeline 2 csv representation.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/paeon
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


class CsvTimeline2(FileExport):
    """File representation of a csv file exported by Aeon Timeline 2. 

    Represents a csv file with a record per scene.
    - Records are separated by line breaks.
    - Data fields are delimited by the _SEPARATOR character.
    """

    EXTENSION = '.csv'
    DESCRIPTION = 'Aeon Timeline CSV export'
    SUFFIX = ''

    _SEPARATOR = ','

    # Events marked as "Scene" become
    # regular scenes, the others become Notes scenes.

    def __init__(self, filePath, **kwargs):
        """Extend the superclass constructor,
        defining instance variables.
        """
        FileExport.__init__(self, filePath, **kwargs)
        self.sceneMarker = kwargs['scene_marker']
        self.sceneLabel = kwargs['scene_label']
        self.descriptionLabel = kwargs['description_label']
        self.notesLabel = kwargs['notes_label']
        self.locationLabel = kwargs['location_label']
        self.itemLabel = kwargs['item_label']
        self.characterLabel = kwargs['character_label']

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
                internalDelimiter = '|'

                for label in [self.sceneLabel, 'Title', 'Start Date', 'End Date']:

                    if not label in reader.fieldnames:
                        return 'ERROR: Label "' + label + '" is missing in the CSV file.'

                scIdsByDate = {}
                eventCount = 0

                for row in reader:
                    eventCount += 1
                    scId = str(eventCount)
                    self.scenes[scId] = Scene()
                    self.scenes[scId].title = row['Title']

                    # Set scene status = "Outline".

                    self.scenes[scId].status = 1

                    #--- Make non-scene events "Note" type scenes.

                    self.scenes[scId].isNotesScene = True

                    if self.sceneMarker in row[self.sceneLabel]:
                        self.scenes[scId].isNotesScene = False

                    if not row['Start Date'] in scIdsByDate:
                        scIdsByDate[row['Start Date']] = []

                    scIdsByDate[row['Start Date']].append(scId)
                    startDateTime = row['Start Date'].split(' ')
                    startYear = int(startDateTime[0].split('-')[0])

                    if len(startDateTime) > 2 or startYear < 100:

                        # Substitute date/time, so yWriter would not prefix them with '19' or '20'.

                        self.scenes[scId].date = Scene.NULL_DATE
                        self.scenes[scId].time = Scene.NULL_TIME

                    else:
                        self.scenes[scId].date = startDateTime[0]
                        self.scenes[scId].time = startDateTime[1]

                        # Calculate duration of scenes that begin after 99-12-31.

                        sceneStart = datetime.fromisoformat(row['Start Date'])
                        sceneEnd = datetime.fromisoformat(row['End Date'])
                        sceneDuration = sceneEnd - sceneStart
                        lastsHours = sceneDuration.seconds // 3600
                        lastsMinutes = (sceneDuration.seconds % 3600) // 60

                        self.scenes[scId].lastsDays = str(sceneDuration.days)
                        self.scenes[scId].lastsHours = str(lastsHours)
                        self.scenes[scId].lastsMinutes = str(lastsMinutes)

                    if self.descriptionLabel in row:
                        self.scenes[scId].desc = row[self.descriptionLabel]

                    if self.notesLabel in row:
                        self.scenes[scId].sceneNotes = row[self.notesLabel]

                    if 'Tags' in row and row['Tags'] != '':
                        self.scenes[scId].tags = row['Tags'].split(internalDelimiter)

                    if self.locationLabel in row:
                        self.scenes[scId].locations = get_lcIds(row[self.locationLabel].split(internalDelimiter))

                    if self.characterLabel in row:
                        self.scenes[scId].characters = get_crIds(row[self.characterLabel].split(internalDelimiter))

                    if self.itemLabel in row:
                        self.scenes[scId].items = get_itIds(row[self.itemLabel].split(internalDelimiter))

        except(FileNotFoundError):
            return 'ERROR: "' + os.path.normpath(self.filePath) + '" not found.'

        except(KeyError):
            return 'ERROR: Wrong csv structure.'

        except(ValueError):
            return 'ERROR: Wrong date/time format.'

        except:
            return 'ERROR: Can not parse "' + os.path.normpath(self.filePath) + '".'

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

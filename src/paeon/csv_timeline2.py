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

    NULL_DATE = '0001-01-01'
    NULL_TIME = '00:00:00'

    # Events marked as "Scene" become
    # regular scenes, the others become Notes scenes.

    def __init__(self, filePath, **kwargs):
        """Extend the superclass constructor,
        defining instance variables.
        """
        FileExport.__init__(self, filePath, **kwargs)
        self.sceneMarker = kwargs['scene_marker']
        self.titleLabel = kwargs['title_label']
        self.sceneLabel = kwargs['scene_label']
        self.startDateTimeLabel = kwargs['start_date_time_label']
        self.endDateTimeLabel = kwargs['end_date_time_label']
        self.descriptionLabel = kwargs['description_label']
        self.notesLabel = kwargs['notes_label']
        self.tagLabel = kwargs['tag_label']
        self.locationLabel = kwargs['location_label']
        self.itemLabel = kwargs['item_label']
        self.characterLabel = kwargs['character_label']
        self.viewpointLabel = kwargs['viewpoint_label']
        self.importAllEvents = kwargs['import_all_events']

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

                for label in [self.sceneLabel, self.titleLabel, self.startDateTimeLabel, self.endDateTimeLabel]:

                    if not label in reader.fieldnames:
                        return 'ERROR: Label "' + label + '" is missing in the CSV file.'

                scIdsByDate = {}
                eventCount = 0

                for row in reader:
                    eventCount += 1

                    if self.sceneMarker == '':
                        noScene = False

                    elif not self.sceneMarker in row[self.sceneLabel]:
                        noScene = True

                        if not self.importAllEvents:
                            continue

                    else:
                        noScene = False

                    scId = str(eventCount)
                    self.scenes[scId] = Scene()
                    self.scenes[scId].isNotesScene = noScene
                    self.scenes[scId].title = row[self.titleLabel]

                    if not row[self.startDateTimeLabel] in scIdsByDate:
                        scIdsByDate[row[self.startDateTimeLabel]] = []

                    scIdsByDate[row[self.startDateTimeLabel]].append(scId)
                    startDateTime = row[self.startDateTimeLabel].split(' ')
                    startYear = int(startDateTime[0].split('-')[0])

                    if len(startDateTime) > 2 or startYear < 100:

                        # Substitute date/time, so yWriter would not prefix them with '19' or '20'.

                        self.scenes[scId].date = self.NULL_DATE
                        self.scenes[scId].time = self.NULL_TIME

                    else:
                        self.scenes[scId].date = startDateTime[0]
                        self.scenes[scId].time = startDateTime[1]

                        # Calculate duration of scenes that begin after 99-12-31.

                        sceneStart = datetime.fromisoformat(row[self.startDateTimeLabel])
                        sceneEnd = datetime.fromisoformat(row[self.endDateTimeLabel])
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

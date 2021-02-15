"""Aeon3 timeline base class

Part of the paeon project (https://github.com/peter88213/paeon)
Copyright (c) 2021 Peter Triesberger
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from abc import abstractmethod
from urllib.parse import quote
import os


class Timeline(object):
    """Abstract Aeon Timeline 3 project file representation.

    This class represents a file containing a timeline with additional 
    attributes and structural information (a full set or a subset
    of the information included in an Aeon Timeline project file).
    """

    DESCRIPTION = 'Timeline'
    EXTENSION = None
    SUFFIX = None
    # To be extended by file format specific subclasses.

    def __init__(self, filePath):
        self.events = {}
        # dict
        # key: Display ID, value: Event.

        self.stories = {}
        # dict
        # key: Display ID, value: Story.

        self.Persons = {}
        # dict
        # key: Display ID, value: Person.

        self._filePath = None
        # str
        # Path to the file. The setter only accepts files of a
        # supported type as specified by EXTENSION.

        self.filePath = filePath

    @property
    def filePath(self):
        return self._filePath

    @filePath.setter
    def filePath(self, filePath):
        """Accept only filenames with the right extension. """

        if self.SUFFIX is not None:
            suffix = self.SUFFIX

        else:
            suffix = ''

        if filePath.lower().endswith(suffix + self.EXTENSION):
            self._filePath = filePath
            head, tail = os.path.split(os.path.realpath(filePath))
            self.projectPath = quote(head.replace('\\', '/'), '/:')
            self.projectName = quote(tail.replace(
                suffix + self.EXTENSION, ''))

    @abstractmethod
    def read(self):
        """Parse the file and store selected properties.
        To be overwritten by file format specific subclasses.
        """

    @abstractmethod
    def merge(self, novel):
        """Copy required attributes of the timeline object.
        To be overwritten by file format specific subclasses.
        """

    @abstractmethod
    def write(self):
        """Write selected properties to the file.
        To be overwritten by file format specific subclasses.
        """

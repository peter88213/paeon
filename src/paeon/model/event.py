"""Event - represents an event in timeline.

Part of the paeon project (https://github.com/peter88213/paeon)
Copyright (c) 2021 Peter Triesberger
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from paeon.model.timeline_element import TimelineElement


class Event(TimelineElement):
    """Timeline event representation.
    """

    def __init__(self):
        TimelineElement.__init__(self)

        self.summary = None
        # str

        self.startDate = None
        # str

        self.startTime = None
        # str

        self.endDate = None
        # str

        self.endTime = None
        # str

        self.tags = None
        # list of str

        self.participants = None
        # list of str
        # list of person's display IDs

        self.witnesses = None
        # list of str
        # list of person's display IDs

        self.stories = None
        # list of str
        # list of story's display IDs

        self.narrativePosition = None
        # list of integer
        # Element 0 = scene no., Element 1 = place in scene.

"""TimelineElement - represents the basic structure of an element in timeline.

Part of the paeon project (https://github.com/peter88213/paeon)
Copyright (c) 2021 Peter Triesberger
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""


class TimelineElement():
    """Abstract timeline element representation.
    """

    def __init__(self):
        self.displayID = None
        # str

        self.label = None
        # str

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

        self.witnesses = None
        # list of str

        self.stories = None
        # list of str

"""Unit tests for of the Aeon3Calendar time extraction methods.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/aeon3obsidian
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import unittest

from aeon2_calendar import Aeon2Calendar


class TestCalendar(unittest.TestCase):

    def setUp(self):
        jsonCalendar = {
            "dateFormat": "medium",
            "dateFormatIncludeDayName": True,
            "displayType": "Absolute",
            "eras": [
                {
                    "duration": 2147483647,
                    "hasLeapYears": False,
                    "index": 0,
                    "isBackwards": True,
                    "name": "BC",
                    "shortName": "BC"
                },
                {
                    "duration": 2147483647,
                    "hasLeapYears": True,
                    "index": 1,
                    "isBackwards": False,
                    "name": "AD",
                    "shortName": "AD"
                }
            ],
            "hoursInDay": 24,
            "months": [
                {
                    "index": 0,
                    "leapDuration": 31,
                    "name": "January",
                    "normalDuration": 31,
                    "shortName": "Jan"
                },
                {
                    "index": 1,
                    "leapDuration": 29,
                    "name": "February",
                    "normalDuration": 28,
                    "shortName": "Feb"
                },
                {
                    "index": 2,
                    "leapDuration": 31,
                    "name": "March",
                    "normalDuration": 31,
                    "shortName": "Mar"
                },
                {
                    "index": 3,
                    "leapDuration": 30,
                    "name": "April",
                    "normalDuration": 30,
                    "shortName": "Apr"
                },
                {
                    "index": 4,
                    "leapDuration": 31,
                    "name": "May",
                    "normalDuration": 31,
                    "shortName": "May"
                },
                {
                    "index": 5,
                    "leapDuration": 30,
                    "name": "June",
                    "normalDuration": 30,
                    "shortName": "Jun"
                },
                {
                    "index": 6,
                    "leapDuration": 31,
                    "name": "July",
                    "normalDuration": 31,
                    "shortName": "Jul"
                },
                {
                    "index": 7,
                    "leapDuration": 31,
                    "name": "August",
                    "normalDuration": 31,
                    "shortName": "Aug"
                },
                {
                    "index": 8,
                    "leapDuration": 30,
                    "name": "September",
                    "normalDuration": 30,
                    "shortName": "Sep"
                },
                {
                    "index": 9,
                    "leapDuration": 31,
                    "name": "October",
                    "normalDuration": 31,
                    "shortName": "Oct"
                },
                {
                    "index": 10,
                    "leapDuration": 30,
                    "name": "November",
                    "normalDuration": 30,
                    "shortName": "Nov"
                },
                {
                    "index": 11,
                    "leapDuration": 31,
                    "name": "December",
                    "normalDuration": 31,
                    "shortName": "Dec"
                }
            ],
            "name": "Standard Calendar",
            "notes": "",
            "timeFormat": "24",
            "weekdayIndexAtZero": 1,
            "weekdays": [
                {
                    "index": 0,
                    "name": "Sunday",
                    "shortName": "Sun"
                },
                {
                    "index": 1,
                    "name": "Monday",
                    "shortName": "Mon"
                },
                {
                    "index": 2,
                    "name": "Tuesday",
                    "shortName": "Tue"
                },
                {
                    "index": 3,
                    "name": "Wednesday",
                    "shortName": "Wed"
                },
                {
                    "index": 4,
                    "name": "Thursday",
                    "shortName": "Thu"
                },
                {
                    "index": 5,
                    "name": "Friday",
                    "shortName": "Fri"
                },
                {
                    "index": 6,
                    "name": "Saturday",
                    "shortName": "Sat"
                }
            ],
            "zeroDateTimestamp": 60971011200
        }
        self.calendar = Aeon2Calendar(jsonCalendar)
        self.jsonData = {
            "events": [
                {
                    "attachments": [],
                    "color": "B1F23887-3F3D-42A4-948D-3774F39D1196",
                    "displayId": "17",
                    "guid": "D857497B-3FEF-4DE9-8A82-FD7E81490118",
                    "links": [],
                    "locked": False,
                    "priority": 500,
                    "rangeValues": [
                        {
                            "minimumZoom":-1,
                            "position": {
                                "precision": "second",
                                "timestamp": 60971179260
                            },
                            "rangeProperty": "78D60610-FEFD-4422-AE43-D8D0C50819D2",
                            "span": {
                                "minutes": 14
                            }
                        }
                    ],
                    "relationships": [
                        {
                            "entity": "673BC035-785F-4A4F-8434-848427C154E2",
                            "percentAllocated": 1,
                            "role": "3A287673-A132-4E23-ACD1-710A9B9EBBBE"
                        },
                        {
                            "entity": "874BF8AD-5F92-4E82-8C1E-9B8A3EC8F63C",
                            "percentAllocated": 1,
                            "role": "C617DC54-46E1-4F59-B90B-333E5B3E5FBF"
                        },
                        {
                            "entity": "8CBD9D4D-12DF-4E27-B42F-91AB33EE1AC2",
                            "percentAllocated": 1,
                            "role": "3A287673-A132-4E23-ACD1-710A9B9EBBBE"
                        },
                        {
                            "entity": "937DEFE3-1D6A-4CC1-A040-728269417E75",
                            "percentAllocated": 1,
                            "role": "C617DC54-46E1-4F59-B90B-333E5B3E5FBF"
                        }
                    ],
                    "tags": [
                        "Alibi"
                    ],
                    "title": "Greta Ohlsson asks Mrs Hubbard for some aspirin",
                    "values": [
                        {
                            "property": "61E0B369-583D-4F81-9CA7-71B692063057",
                            "value": "0"
                        },
                        {
                            "property": "F0342589-DDED-4E65-A1AC-741187746EE0",
                            "value": ""
                        }
                    ]
                }
            ]
        }
        # Get date/time/duration.
        itemUid = 'D857497B-3FEF-4DE9-8A82-FD7E81490118'
        for event in self.jsonData['events']:
            if event['guid'] == itemUid:
                self.itemDates = event

    def test_get_timestamp(self):
        self.assertEqual(self.calendar.get_timestamp(self.itemDates), 60971179260)

    def test_get_era(self):
        self.assertEqual(self.calendar.get_era(self.itemDates), (1, 'AD', 'AD'))

    def test_get_year(self):
        self.assertEqual(self.calendar.get_year(self.itemDates), 1933)

    def test_get_month(self):
        self.assertEqual(self.calendar.get_month(self.itemDates), (2, 'Feb', 'February'))

    def test_get_day(self):
        self.assertEqual(self.calendar.get_day(self.itemDates), 6)

    def test_get_hour(self):
        self.assertEqual(self.calendar.get_hour(self.itemDates), 22)

    def test_get_minute(self):
        self.assertEqual(self.calendar.get_minute(self.itemDates), 41)

    def test_get_second(self):
        self.assertEqual(self.calendar.get_second(self.itemDates), 0)

    def test_get_weekday(self):
        self.assertEqual(self.calendar.get_weekday(self.itemDates), (1, 'Mon', 'Monday'))

    def test_get_iso_date(self):
        self.assertEqual(self.calendar.get_iso_date(self.itemDates), '1933-02-06')

    def test_get_iso_time(self):
        self.assertEqual(self.calendar.get_iso_time(self.itemDates), '22:41:00')

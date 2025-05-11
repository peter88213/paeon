"""Provide a class with helper methods for date/time formatting.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/paeon
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""


class Aeon2Calendar:

    ISO_ERAS = ('AD')

    def __init__(self, calendarDefinitions):

        self.hoursInDay = calendarDefinitions['hoursInDay']
        self.minutesInHour = 60
        self.secondsInMinute = 60
        self.weekdayIndexAtZero = calendarDefinitions['weekdayIndexAtZero']

        #--- Era enumerations.
        self.eraShortNames = []
        self.eraNames = []
        for era in calendarDefinitions['eras']:
            self.eraShortNames.append(era['shortName'])
            self.eraNames.append(era['name'])

        #--- Month enumerations.
        self.monthShortNames = []
        self.monthNames = []
        for month in calendarDefinitions['months']:
            self.monthShortNames.append(month['shortName'])
            self.monthNames.append(month['name'])

        #--- Weekday enumerations.
        self.weekdayShortNames = []
        self.weekdayNames = []
        for weekday in calendarDefinitions['weekdays']:
            self.weekdayShortNames.append(weekday['shortName'])
            self.weekdayNames.append(weekday['name'])

    def get_day(self, itemDates):
        """Return an integer day or None."""
        timestamp = itemDates['rangeValues'][0]['position']['timestamp']
        if timestamp is not None:
            return timestamp.get('day', None)

    def get_duration_str(self, itemDates):
        """Return a string with comma-separated elements of the duration."""
        durationList = []
        durationDict = itemDates.get('duration', None)
        if durationDict:
            durations = list(durationDict)
            for unit in durations:
                if durationDict[unit]:
                    durationList.append(f'{durationDict[unit]} {unit}')
        durationStr = ', '.join(durationList)
        return durationStr

    def get_era(self, itemDates):
        """Return a tuple: (era as an integer, era's short name, era's name)."""

        try:
            return era, self.eraShortNames[era], self.eraNames[era]
        except:
            return

    def get_hour(self, itemDates):
        """Return an integer hour or None."""
        timestamp = self.get_timestamp(itemDates)
        if timestamp is None:
            return

        minutesTotal = timestamp // self.secondsInMinute
        hoursTotal = minutesTotal // self.minutesInHour
        daysTotal = hoursTotal // self.hoursInDay
        return hoursTotal % daysTotal

    def get_iso_date(self, itemDates):
        """Return a date string formatted acc. to ISO 8601, if applicable. 
        
        Return None, if the date isn't within the range specified by ISO 8601, 
        or in case of error.
        """
        try:
            timestamp = itemDates['timestamp']
            era = timestamp['era']
            eraName = self.eraNames[era]
            if eraName not in self.ISO_ERAS:
                return

            year = timestamp['year']
            month = timestamp['month']
            day = timestamp['day']
            return f'{year:04}-{month:02}-{day:02}'
        except:
            return

    def get_iso_time(self, itemDates):
        """Return a time string formatted acc. to ISO 8601. 
        
        Return None in case of error.
        """
        try:
            hour = self.get_hour(itemDates)
            minute = self.get_minute(itemDates)
            second = self.get_second(itemDates)
            return f'{hour:02}:{minute:02}:{second:02}'
        except:
            return

    def get_minute(self, itemDates):
        """Return an integer minute or None."""
        timestamp = self.get_timestamp(itemDates)
        if timestamp is None:
            return

        minutesTotal = timestamp // self.secondsInMinute
        hoursTotal = minutesTotal // self.minutesInHour
        return minutesTotal % hoursTotal

    def get_month(self, itemDates):
        """Return a tuple: (month's order, month's short name, month's name)."""
        timestamp = itemDates['rangeValues'][0]['position']['timestamp']
        if timestamp is None:
            return

        month = timestamp.get('month', None)
        if month is None:
            return

        try:
            return month, self.monthShortNames[month - 1], self.monthNames[month - 1]
        except:
            return

    def get_second(self, itemDates):
        """Return an integer second or None."""
        timestamp = self.get_timestamp(itemDates)
        if timestamp is None:
            return

        return timestamp % self.secondsInMinute

    def get_timestamp(self, itemDates):
        """Return an integer timestamp or None."""
        return itemDates['rangeValues'][0]['position']['timestamp']

    def get_weekday(self, itemDates):
        """Return a tuple: (weekday as an integer, weekday's short name, weekday's name)."""
        timestamp = self.get_timestamp(itemDates)
        if timestamp is None:
            return

        minutesTotal = timestamp // self.secondsInMinute
        hoursTotal = minutesTotal // self.minutesInHour
        daysTotal = hoursTotal // self.hoursInDay
        try:
            weekdayOffset = self.weekdayIndexAtZero
            # Note: this works only for the final era
            # TODO: consider preceding eras by length and direction
            weekday = (daysTotal % len(self.weekdayNames)) + weekdayOffset
            return weekday, self.weekdayShortNames[weekday], self.weekdayNames[weekday]
        except:
            return

    def get_year(self, itemDates):
        """Return an integer year or None."""
        timestamp = itemDates['rangeValues'][0]['position']['timestamp']
        if timestamp is not None:
            return timestamp.get('year', None)


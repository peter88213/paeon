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
        self.secondsInDay = self.secondsInMinute * self.minutesInHour * self.hoursInDay

        daysInNormalYear = 0
        daysInLeapYear = 0
        self.monthNormalDurations = []
        self.monthLeapDurations = []
        self.monthShortNames = []
        self.monthNames = []
        for month in calendarDefinitions['months']:
            daysInNormalYear += month['normalDuration']
            self.monthNormalDurations.append(month['normalDuration'])
            daysInLeapYear += month['leapDuration']
            self.monthLeapDurations.append(month['leapDuration'])
            self.monthShortNames.append(month['shortName'])
            self.monthNames.append(month['name'])
        self.secondsInYear = daysInNormalYear * self.secondsInDay
        self.secondsInLeapYear = daysInLeapYear * self.secondsInDay

        self.weekdayIndexAtZero = calendarDefinitions['weekdayIndexAtZero']
        self.leapCycles = [4, 100, 400]

        #--- Era enumerations.
        self.eraShortNames = []
        self.eraNames = []
        self.eraSeconds = []
        for self.maxEra, era in enumerate(calendarDefinitions['eras']):
            self.eraShortNames.append(era['shortName'])
            self.eraNames.append(era['name'])
            self.eraSeconds.append(era['duration'] * self.secondsInYear)

        #--- Weekday enumerations.
        self.weekdayShortNames = []
        self.weekdayNames = []
        for weekday in calendarDefinitions['weekdays']:
            self.weekdayShortNames.append(weekday['shortName'])
            self.weekdayNames.append(weekday['name'])

    def get_date(self, itemDates):
        timestamp = self.get_timestamp(itemDates)
        if timestamp is None:
            return

        maxSeconds = abs(timestamp)

        #--- Year.
        year = 1
        if self.isleap(year):
            seconds = self.secondsInLeapYear
        else:
            seconds = self.secondsInYear
        secondsCurrentYear = maxSeconds - seconds
        while seconds <= maxSeconds:
            secondsCurrentYear = maxSeconds - seconds
            year += 1
            if self.isleap(year):
                seconds += self.secondsInLeapYear
            else:
                seconds += self.secondsInYear

        #--- Month.
        isLeapYear = self.isleap(year)
        monthIndex = 0
        if isLeapYear:
            days = self.monthLeapDurations[monthIndex]
        else:
            days = self.monthNormalDurations[monthIndex]
        seconds = self.secondsInDay * days
        secondsCurrentMonth = secondsCurrentYear - seconds
        while seconds < secondsCurrentYear:
            secondsCurrentMonth = secondsCurrentYear - seconds
            monthIndex += 1
            if isLeapYear:
                days = self.monthLeapDurations[monthIndex]
            else:
                days = self.monthNormalDurations[monthIndex]
            seconds += self.secondsInDay * days

        #--- Day.
        dayIndex = secondsCurrentMonth // self.secondsInDay

        return year, monthIndex + 1, dayIndex + 1

    def get_day(self, itemDates):
        """Return an integer day or None."""
        _, _, day = self.get_date(itemDates)
        return day

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
        timestamp = self.get_timestamp(itemDates)
        era = self.maxEra
        eraStart = 0
        if timestamp < 0:
            era -= 1
            eraStart -= self.eraSeconds[era]
            while timestamp < eraStart:
                era -= 1
                eraStart -= self.eraSeconds[era]
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
        _, eraShortName, _ = self.get_era(itemDates)
        if eraShortName not in self.ISO_ERAS:
            return

        year = self.get_year(itemDates)
        month, _, _ = self.get_month(itemDates)
        day = self.get_day(itemDates)
        return f'{year:04}-{month:02}-{day:02}'

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
        _, month, _ = self.get_date(itemDates)
        try:
            return (
                month,
                self.monthShortNames[month - 1],
                self.monthNames[month - 1],
                )
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
        year, _, _ = self.get_date(itemDates)
        return  year

    def isleap(self, year):
        """Return True if year is a leap year."""
        return ((year % self.leapCycles[2] == 0) and (year % self.leapCycles[1] == 0)
                or (year % self.leapCycles[0] == 0) and (year % self.leapCycles[1] != 0))

    def leapyears(self, y1, y2):
        """Return number of leap years in range [y1, y2). Assume y1 <= y2."""
        y1 -= 1
        y2 -= 1
        return (y2 // self.leapCycles[0] - y1 // self.leapCycles[0]
                ) - (y2 // self.leapCycles[1] - y1 // self.leapCycles[1]
                     ) + (y2 // self.leapCycles[2] - y1 // self.leapCycles[2])

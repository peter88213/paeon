"""Unit tests for of the Aeon2Calendar date calculation methods.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/paeon
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import unittest

import calendar


def isleap(year, leapCycles):
    """Return True if year is a leap year."""
    return ((year % leapCycles[2] == 0) and (year % leapCycles[1] == 0)
            or (year % leapCycles[0] == 0) and (year % leapCycles[1] != 0))


def leapyears(y1, y2, leapCycles):
    """Return number of leap years in range [y1, y2). Assume y1 <= y2."""
    y1 -= 1
    y2 -= 1
    return (y2 // leapCycles[0] - y1 // leapCycles[0]
            ) - (y2 // leapCycles[1] - y1 // leapCycles[1]
                ) + (y2 // leapCycles[2] - y1 // leapCycles[2])


class Test(unittest.TestCase):

    def testLeapYears(self):
        leapCycles = [4, 100, 400]
        for year in range (0, 9999):
            self.assertEqual(isleap(year, leapCycles), calendar.isleap(year))

    def testLeapDays(self):
        leapCycles = [4, 100, 400]
        for year in range (0, 2026):
            self.assertEqual(leapyears(year, 2025, leapCycles), calendar.leapdays(year, 2025))


if __name__ == "__main__":
    unittest.main()

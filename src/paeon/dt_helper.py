"""Provide helper functions for date/time processing.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/aeon3yw
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""


def fix_iso_dt(dateTimeStr):
    """Return a date/time string with a four-number year.
    This is required for comparing date/time strings, 
    and by the datetime.fromisoformat() method.

    Substitute missing time by "00:00:00".
    If the date is empty or out of yWriter's range, return None. 
    """
    if not dateTimeStr:
        return None

    if dateTimeStr.startswith('BC'):
        return None

    dt = dateTimeStr.split('-', 1)

    if int(dt[0]) < 100:
        return None

    if int(dt[0]) > 9999:
        return None

    dt[0] = dt[0].zfill(4)
    dateTimeStr = ('-').join(dt)

    if not ':' in dateTimeStr:
        dateTimeStr += ' 00:00:00'

    return dateTimeStr

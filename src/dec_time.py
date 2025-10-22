"""Calculate alternate start times for Aeon Timeline.

Requires Python 3.7+

Calculates the start time based on the decimal system: 
100 ticks to a minim,  10 minims to an interval, 10 intervals to a day.

1. Read CSV file exported by Aeon Timeline.
2. Calculate and fill in alternate dates.
3. Update the CSV file for Aeon Timeline import.

Usage: dec_time.py path-to-csv-file

This also works via dragging/dropping the csv file onto the script's icon.

Copyright (c) 2025 Peter Triesberger
https://github.com/peter88213/paeon
Published under the MIT License 
(https://opensource.org/licenses/mit-license.php)
"""
import sys
import csv
from datetime import time
from datetime import datetime

ALTERNATE_DATE_TIME_LABEL = 'Decimal Time'


def calculate_alternate_date(dt_str):
    # Calculate the alternate date from the iso 6801:2004 date/time string.
    dt = dt_str.split(' ')
    for timestring in dt:
        if ':' in timestring:
            try:
                timeobj = time.fromisoformat(timestring)
                seconds = (
                    timeobj.hour * 3600 +
                    timeobj.minute * 60 +
                    timeobj.second
                )
                interval, seconds = divmod(seconds, 8640)
                minim, seconds = divmod(seconds, 864)
                tick = int(seconds / 8.64)
            except:
                return ''

            return f'{interval:02}:{minim:02}:{tick:02}'


def main(csvfile_path):
    aeon_data = read_csv(csvfile_path)
    for row in aeon_data:
        dt_str = (row['Start Date'])
        try:
            row[ALTERNATE_DATE_TIME_LABEL] = calculate_alternate_date(
                convert_bc_to_iso_6801(dt_str)
            )
        except:
            pass
    write_csv(csvfile_path, aeon_data)


def read_csv(csvfile_path):
    aeon_data = []
    with open(csvfile_path, 'r', encoding='utf-8', newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            aeon_data.append(row)
    return aeon_data


def write_csv(csvfile_path, aeon_data):
    with open(csvfile_path, 'w', encoding='utf-8', newline='') as csvfile:
        csv_writer = csv.DictWriter(
            csvfile,
            list(aeon_data[0]),
            quoting=csv.QUOTE_ALL,
        )
        csv_writer.writeheader()
        for row in aeon_data:
            csv_writer.writerow(row)


def convert_bc_to_iso_6801(dt_str):
    # Return dt_str with negative date or year zero, if applicable.
    if not dt_str.startswith('BC'):
        return dt_str

    # Convert "BC" year to negative year, starting with zero.
    dt_split = dt_str.split(' ')
    date_str = dt_split[1]
    dt = datetime.fromisoformat(date_str)
    year = -1 * (dt.year - 1)
    iso_6801_dt_str = '-'.join([
        str(year).zfill(4),
        str(dt.month).zfill(2),
        str(dt.day).zfill(2)
    ])
    try:
        iso_6801_dt_str = f'{iso_6801_dt_str} {dt_split[2]}'
    except:
        pass
    return iso_6801_dt_str


if __name__ == '__main__':
    main(sys.argv[1])

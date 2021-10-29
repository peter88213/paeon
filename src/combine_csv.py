#!/usr/bin/env python3
"""Combine csv files

Requires Python 3.7 or above

Copyright (c) 2021 Peter Triesberger
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import csv

RESULT = 'combined.csv'

directory = os.getcwd()
result = []
labels = []

# Read all csv files in the working directory and collect the rows in result.

for filename in os.listdir(directory):

    if filename.endswith('.csv') and filename != RESULT:
        print('Reading ' + filename)

        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)

            for label in reader.fieldnames:

                if not label in labels:
                    labels.append(label)

            for row in reader:
                result.append(row)

if len(result):

    # Write result to a new csv file.

    with open(RESULT, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=labels, quoting=csv.QUOTE_ALL)
        writer.writeheader()

        for row in result:
            writer.writerow(row)

        print(RESULT + ' written.')

else:
    print('No csv file found.')

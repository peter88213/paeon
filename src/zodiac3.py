#!/usr/bin/python3
"""Insert zodiac calendar eras into an Aeon Timeline 3 template.

usage:

zodiac3.py path-to-template

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import sys
import json

NUMBER_OF_YEARS = 1000
FIRST_ERA_NAME = 'Before the Big Divide'
FIRST_ERA_SHORT_NAME = 'Before the Big Divide'
LAST_ERA_NAME = 'Unknown Future'
LAST_ERA_SHORT_NAME = 'UF'

ZODIAC_SIGNS = ['♈', '♉', '♊', '♋', '♌', '♍', '♎', '♏', '♐', '♑', '♒', '♓']
ZODIAC_NAMES = [
    'Aries',
    'Taurus',
    'Gemini',
    'Cancer',
    'Leo',
    'Virgo',
    'Libra',
    'Scorpio',
    'Sagittarius',
    'Capricorn',
    'Aquarius',
    'Pisces'
]
ELEMENTS = ['Water', 'Fire', 'Wood', 'Air']


def get_zodiac_year(calendarYear):
    absoluteYear = calendarYear - 1
    # because the calendars begins with Year One
    absoluteEra = absoluteYear // len(ZODIAC_SIGNS)
    element = absoluteEra % len(ELEMENTS)
    zodiacYear = absoluteYear % len(ZODIAC_SIGNS)
    zodiacEra = absoluteEra + 1
    return zodiacEra, element, zodiacYear


def main(templatePath):

    def get_era(name, shortName, duration):
        return {
            'name': name,
            'shortName': shortName,
            'isBackwards': False,
            'hasLeapYears': False,
            'leapOffset': 0,
            'duration': str(duration)
        }

    with open(templatePath, 'r', encoding='utf-8') as f:
        jsonTemplate = json.load(f)
    jsonEras = [
        {
          'name': FIRST_ERA_NAME,
          'shortName': FIRST_ERA_SHORT_NAME,
          'isBackwards': True,
          'hasLeapYears': True,
          'leapOffset': 1,
          'duration': 9007199254740992
        }
    ]
    calendarYear = 1
    for _ in range(NUMBER_OF_YEARS):
        zodiacEra, element, zodiacYear = get_zodiac_year(calendarYear)
        zName = f'{ZODIAC_NAMES[zodiacYear]}, Era {zodiacEra} "Era of {ELEMENTS[element]}"'
        zShortName = f'{ZODIAC_SIGNS[zodiacYear]}, Era {zodiacEra} "{ELEMENTS[element]}"'
        jsonEras.append(get_era(zName, zShortName, 1))
        calendarYear += 1
    jsonEras.append(get_era(LAST_ERA_NAME, LAST_ERA_SHORT_NAME, 9007199254740992))
    jsonTemplate['definitions']['calendar']['eras'] = jsonEras
    filePath, _ = os.path.split(templatePath)
    newTemplate = os.path.join(filePath, 'zodiac.aeonTpl')
    with open(newTemplate, 'w', encoding='utf-8') as f:
        json.dump(jsonTemplate, f)
    print(f'New template "{newTemplate}" written')


if __name__ == '__main__':
    main(sys.argv[1])

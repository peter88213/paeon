#!/usr/bin/python3
"""Insert zodiac calendar eras into an Aeon Timeline 2 template.

usage:

zodiac.py path-to-template

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import sys
import xml.etree.ElementTree as ET

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

    def add_era(name, shortName, duration):
        newEra = ET.SubElement(xmlEras, 'Era')
        ET.SubElement(newEra, 'Name').text = name
        ET.SubElement(newEra, 'ShortName').text = shortName
        ET.SubElement(newEra, 'Index').text = str(index)
        ET.SubElement(newEra, 'Duration').text = str(duration)
        ET.SubElement(newEra, 'IsBackwards').text = '0'
        ET.SubElement(newEra, 'HasLeapYears').text = '0'

    xmlTree = ET.parse(templatePath)
    xmlTemplate = xmlTree.getroot()
    xmlRangeProperties = xmlTemplate.find('RangeProperties')
    xmlRangeProperty = xmlRangeProperties.find('RangeProperty')
    xmlCalendar = xmlRangeProperty.find('Calendar')
    xmlEras = xmlCalendar.find('Eras')
    for xmlEra in xmlEras.iterfind('Era'):
        if xmlEra.find('Name').text == 'BC':
            xmlEra.find('Name').text = FIRST_ERA_NAME
            xmlEra.find('ShortName').text = FIRST_ERA_SHORT_NAME
        else:
            xmlEras.remove(xmlEra)
    calendarYear = 1
    index = 1
    for _ in range(NUMBER_OF_YEARS):
        zodiacEra, element, zodiacYear = get_zodiac_year(calendarYear)
        zName = f'{ZODIAC_NAMES[zodiacYear]}, Era {zodiacEra} "Era of {ELEMENTS[element]}"'
        zShortName = f'{ZODIAC_SIGNS[zodiacYear]}, Era {zodiacEra} "{ELEMENTS[element]}"'
        add_era(zName, zShortName, 1)
        index += 1
        calendarYear += 1
    add_era(LAST_ERA_NAME, LAST_ERA_SHORT_NAME, 9007199254740992)
    filePath, _ = os.path.split(templatePath)
    newTemplate = os.path.join(filePath, 'zodiac.xml')
    ET.indent(xmlTree)
    xmlTree.write(newTemplate, xml_declaration=True, encoding='utf-8')
    print(f'New template "{newTemplate}" written')


if __name__ == '__main__':
    main(sys.argv[1])

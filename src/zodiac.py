#!/usr/bin/python3
"""Create zodiac calendar eras for an Aeon Timeline 2 template

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import calendar
import sys
import xml.etree.ElementTree as ET

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
    # because the calendas begins with Year One
    absoluteEra = absoluteYear // len(ZODIAC_SIGNS)
    element = absoluteEra % len(ELEMENTS)
    zodiacYear = absoluteYear % len(ZODIAC_SIGNS)
    zodiacEra = absoluteEra + 1
    return zodiacEra, element, zodiacYear


def print_years(first, number):
    for y in range(number):
        calendarYear = first + y
        zodiacEra, element, zodiacYear = get_zodiac_year(calendarYear)
        print(f'{calendarYear} {ZODIAC_SIGNS[zodiacYear]}, Era {zodiacEra} "Era of {ELEMENTS[element]}"')


def main(templatePath):

    def add_era(name, shortName, duration):
        newEra = ET.SubElement(xmlEras, 'Era')
        ET.SubElement(newEra, 'Name').text = name
        ET.SubElement(newEra, 'ShortName').text = shortName
        ET.SubElement(newEra, 'Index').text = str(index)
        ET.SubElement(newEra, 'Duration').text = str(duration)
        ET.SubElement(newEra, 'IsBackwards').text = '0'
        ET.SubElement(newEra, 'HasLeapYears').text = '0'

    startYear = 1967
    numberOfYears = 144

    xmlTree = ET.parse(templatePath)
    xmlTemplate = xmlTree.getroot()
    xmlRangeProperties = xmlTemplate.find('RangeProperties')
    xmlRangeProperty = xmlRangeProperties.find('RangeProperty')
    xmlCalendar = xmlRangeProperty.find('Calendar')
    xmlEras = xmlCalendar.find('Eras')
    index = 0
    for xmlEra in xmlEras.iterfind('Era'):
        xmlName = xmlEra.find('Name')
        if xmlName.text == 'AD':
            xmlEra.find('Duration').text = str(startYear - 1)
        index += 1
    calendarYear = startYear
    for _ in range(numberOfYears):
        zodiacEra, element, zodiacYear = get_zodiac_year(calendarYear)
        zName = f'{ZODIAC_NAMES[zodiacYear]}, Era {zodiacEra} "Era of {ELEMENTS[element]}"'
        zShortName = f'{ZODIAC_SIGNS[zodiacYear]}, Era {zodiacEra} "Era of {ELEMENTS[element]}"'
        add_era(zName, zShortName, 1)
        index += 1
        calendarYear += 1
    add_era('End Age', 'End Age', 9007199254740992)
    filePath, _ = os.path.split(templatePath)
    newTemplate = os.path.join(filePath, 'zodiac.xml')
    ET.indent(xmlTree)
    xmlTree.write(newTemplate, xml_declaration=True, encoding='utf-8')
    print(f'New template "{newTemplate}" written')


if __name__ == '__main__':
    main(sys.argv[1])

#!/usr/bin/python3
"""Insert zodiac calendar eras into an Aeon Timeline 2 template.

usage:

zodiac_eras.py path-to-template

Copyright (c) 2024 Peter Triesberger
For further information see https://peter88213.github.io/paeon/zodiac
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import sys
import xml.etree.ElementTree as ET

NUMBER_OF_ERAS = 98
FIRST_ERA_NAME = 'Before the Big Divide'
FIRST_ERA_SHORT_NAME = 'Before the Big Divide'
LAST_ERA_NAME = 'Unknown Future'
LAST_ERA_SHORT_NAME = 'UF'
YEARS_PER_ERA = 12
ELEMENTS = ['Water', 'Fire', 'Wood', 'Air']


def get_zodiac_era(era):
    element = era % len(ELEMENTS)
    zodiacEra = era + 1
    return zodiacEra, element


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
    index = 1
    for era in range(NUMBER_OF_ERAS):
        zodiacEra, element = get_zodiac_era(era)
        zName = f'Era {zodiacEra} "Era of {ELEMENTS[element]}"'
        zShortName = f'Era {zodiacEra} "{ELEMENTS[element]}"'
        add_era(zName, zShortName, YEARS_PER_ERA)
        index += 1
    add_era(LAST_ERA_NAME, LAST_ERA_SHORT_NAME, 9007199254740992)
    filePath, _ = os.path.split(templatePath)
    newTemplate = os.path.join(filePath, 'zodiac-eras.xml')
    ET.indent(xmlTree)
    xmlTree.write(newTemplate, xml_declaration=True, encoding='utf-8')
    print(f'New template "{newTemplate}" written')


if __name__ == '__main__':
    main(sys.argv[1])

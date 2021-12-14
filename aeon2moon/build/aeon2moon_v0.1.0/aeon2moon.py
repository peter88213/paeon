#!/usr/bin/env python3
"""Aeon Timeline 2 moon phase at event start date.

Version 0.1.0

usage: aeon2moon.py [-h] Sourcefile

positional arguments:
  Sourcefile  The path of the .aeonzip file.

optional arguments:
  -h, --help  show this help message and exit
  
Add the phase day (0 to 29, where 0=new moon, 15=full etc.) to each event.

Copyright (c) 2021 Peter Triesberger
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import argparse
from datetime import datetime
from datetime import timedelta

import zipfile
import codecs
import json
import os


def open_timeline(filePath):
    """Unzip the project file and read 'timeline.json'.
    Return a message beginning with SUCCESS or ERROR
    and the JSON timeline structure.
    """

    try:
        with zipfile.ZipFile(filePath, 'r') as myzip:
            jsonBytes = myzip.read('timeline.json')
            jsonStr = codecs.decode(jsonBytes, encoding='utf-8')

    except:
        return 'ERROR: Cannot read JSON data.', None

    if not jsonStr:
        return 'ERROR: No JSON part found.', None

    try:
        jsonData = json.loads(jsonStr)

    except('JSONDecodeError'):
        return 'ERROR: Invalid JSON data.'
        None

    return 'SUCCESS', jsonData


def save_timeline(jsonData, filePath):
    """Write the jsonData structure to a zipfile located at filePath.
    Return a message beginning with SUCCESS or ERROR.
    """

    try:

        with zipfile.ZipFile(filePath, 'w') as f:
            f.writestr('timeline.json', json.dumps(jsonData))

    except:
        return 'ERROR: Cannot write JSON data.'

    return 'SUCCESS: "' + os.path.normpath(filePath) + '" written.'
from hashlib import pbkdf2_hmac

guidChars = list('ABCDEF0123456789')


def get_sub_guid(key, size):
    """Create string from a bytes key.
    """
    keyInt = int.from_bytes(key, byteorder='big')
    guid = ''

    while len(guid) < size and keyInt > 0:
        guid += guidChars[keyInt % len(guidChars)]
        keyInt //= len(guidChars)

    return guid


def get_uid(text):
    """Return a GUID for Aeon Timeline.

    Form: aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee
    """
    text = text.encode('utf-8')

    sizes = [8, 4, 4, 4, 12]
    salts = [b'a', b'b', b'c', b'd', b'e']
    guid = []

    for i in range(5):
        key = pbkdf2_hmac('sha1', text, salts[i], 1)
        guid.append(get_sub_guid(key, sizes[i]))

    return '-'.join(guid)
import sys
import math


def get_moon_phase(dateStr):

    y, m, d = dateStr.split('-')
    year = int(y)
    month = int(m)
    day = int(d)
    r = year % 100
    r %= 19

    if r > 9:
        r -= 19

    r = ((r * 11) % 30) + month + day

    if month < 3:
        r += 2

    if year < 2000:
        r -= 4

    else:
        r -= 8.3

    r = math.floor(r + 0.5) % 30

    if r < 0:
        r += 30

    return r


def get_moon_phase_plus(dateStr):
    """Return a string containing the moon phase plus a pseudo-graphic display.
    """
    s = '  ))))))))))))OOO(((((((((((( '
    r = get_moon_phase(dateStr)
    return str(r) + ' [  ' + s[r] + '  ]'



VERSION = 'v0.1.0'
AEON2_EXT = '.aeonzip'

PROPERTY_MOONPHASE = 'Moon phase'


def run(sourcePath):
    """Extract JSON data from an .aeonzip file
    and add or update the "Moon phase" property. 
    Return a message beginning with SUCCESS or ERROR.
    """

    if sourcePath.endswith(AEON2_EXT):
        message, jsonData = open_timeline(sourcePath)

        if message.startswith('ERROR'):
            return message

    else:
        return('ERROR: File format not supported.')

    #--- Get the date definition.

    for tplRgp in jsonData['template']['rangeProperties']:

        if tplRgp['type'] == 'date':

            for tplRgpCalEra in tplRgp['calendar']['eras']:

                if tplRgpCalEra['name'] == 'AD':
                    tplDateGuid = tplRgp['guid']
                    break

    if tplDateGuid is None:
        return 'ERROR: "AD" era is missing in the calendar.'

    #--- Get GUID of user defined properties.

    propertyMoonphaseGuid = None

    for tplPrp in jsonData['template']['properties']:

        if tplPrp['name'] == PROPERTY_MOONPHASE:
            propertyMoonphaseGuid = tplPrp['guid']

    #--- Create user defined properties, if missing.

    if propertyMoonphaseGuid is None:
        n = len(jsonData['template']['properties'])
        propertyMoonphaseGuid = get_uid('propertyMoonphaseGuid')
        jsonData['template']['properties'].append({
            'calcMode': 'default',
            'calculate': False,
            'fadeEvents': False,
            'guid': propertyMoonphaseGuid,
            'icon': 'flag',
            'isMandatory': False,
            'name': PROPERTY_MOONPHASE,
            'sortOrder': n,
            'type': 'text'
        })

    for evt in jsonData['events']:

        #--- Get date/time

        timestamp = 0

        for evtRgv in evt['rangeValues']:

            if evtRgv['rangeProperty'] == tplDateGuid:
                timestamp = evtRgv['position']['timestamp']

                try:
                    eventStart = datetime.min + timedelta(seconds=timestamp)
                    startDateTime = eventStart.isoformat().split('T')
                    eventMoonphase = get_moon_phase_plus(startDateTime[0])

                except:
                    eventMoonphase = ''

        #--- Set moon phase.

        hasMoonphase = False

        for evtVal in evt['values']:

            if evtVal['property'] == propertyMoonphaseGuid:
                evtVal['value'] = eventMoonphase
                hasMoonphase = True

        #--- Add missing event properties.

        if not hasMoonphase:
            evt['values'].append({'property': propertyMoonphaseGuid, 'value': eventMoonphase})

    return save_timeline(jsonData, sourcePath)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Aeon Timeline 2 moon phase at event start date ' + VERSION,
        epilog='Add the phase day (0 to 29, where 0=new moon, 15=full etc.) to each event.')
    parser.add_argument('sourcePath', metavar='Sourcefile',
                        help='The path of the .aeonzip file.')

    args = parser.parse_args()
    print(run(args.sourcePath))

#!/usr/bin/python3
"""Aeon Timeline 2 Add/update moon phase at event start date.

Version 0.4.5
Requires Python 3.6+

usage: aeon2moon.py [-h] Sourcefile

positional arguments:
  Sourcefile  The path of the .aeonzip file.

optional arguments:
  -h, --help  show this help message and exit
  
"Moon phase" event property: phase day (0 to 29, where 0=new moon, 15=full etc.)

Copyright (c) 2023 Peter Triesberger
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import argparse
from shutil import copy2
from datetime import datetime
from datetime import timedelta
import os

ERROR = '!'


def _(message):
    return message


import zipfile
import codecs
import json


def open_timeline(filePath):
    """Unzip the project file and read 'timeline.json'.

    Positional arguments:
        filePath -- Path of the .aeon project file to read.
        
    Return a message beginning with the ERROR constant in case of error
    and a Python object containing the timeline structure.
    """
    try:
        with zipfile.ZipFile(filePath, 'r') as myzip:
            jsonBytes = myzip.read('timeline.json')
            jsonStr = codecs.decode(jsonBytes, encoding='utf-8')
    except:
        return f'{ERROR}Cannot read timeline data.', None
    if not jsonStr:
        return f'{ERROR}No JSON part found in timeline data.', None
    try:
        jsonData = json.loads(jsonStr)
    except('JSONDecodeError'):
        return f'{ERROR}Invalid JSON data in timeline.'
        None
    return 'Timeline data read in.', jsonData


def save_timeline(jsonData, filePath):
    """Write the timeline to a zipfile located at filePath.
    
    Positional arguments:
        jsonData -- Python object containing the timeline structure.
        filePath -- Path of the .aeon project file to write.
        
    Return a message beginning with the ERROR constant in case of error.
    """
    if os.path.isfile(filePath):
        os.replace(filePath, f'{filePath}.bak')
        backedUp = True
    else:
        backedUp = False
    try:
        with zipfile.ZipFile(filePath, 'w', compression=zipfile.ZIP_DEFLATED) as f:
            f.writestr('timeline.json', json.dumps(jsonData))
    except:
        if backedUp:
            os.replace(f'{filePath}.bak', filePath)
        return f'{ERROR}Cannot write "{os.path.normpath(filePath)}".'

    return f'"{os.path.normpath(filePath)}" written.'


from hashlib import pbkdf2_hmac

guidChars = list('ABCDEF0123456789')


def get_sub_guid(key, size):
    """Return a string generated from a bytes key.
    
    Positional arguments:
        key -- bytes: key.
        size -- length of the returned string.
    """
    keyInt = int.from_bytes(key, byteorder='big')
    guid = ''
    while len(guid) < size and keyInt > 0:
        guid += guidChars[keyInt % len(guidChars)]
        keyInt //= len(guidChars)
    return guid


def get_uid(text):
    """Return a GUID for Aeon Timeline.
    
    Positional arguments:
        text -- string to generate a GUID from.

    GUID format: aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee
    """
    text = text.encode('utf-8')
    sizes = [8, 4, 4, 4, 12]
    salts = [b'a', b'b', b'c', b'd', b'e']
    guid = []
    for i in range(5):
        key = pbkdf2_hmac('sha1', text, salts[i], 1)
        guid.append(get_sub_guid(key, sizes[i]))
    return '-'.join(guid)


import math


def get_moon_phase(dateStr):
    """Return a single value - the phase day (0 to 29, where 0=new moon, 15=full etc.) 
    for the selected date.
    Date format is 'yyyy-mm-dd'.
    This is based on a 'do it in your head' algorithm by John Conway. 
    In its current form, it's only valid for the 20th and 21st centuries.
    See: http://www.ben-daglish.net/moon.shtml
    """
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
    p = '00¼¼¼¼½½½½¾¾¾¾111¾¾¾¾½½½½¼¼¼¼0'
    r = get_moon_phase(dateStr)
    return f'{r} [  {s[r]}  ] {p[r]}'


VERSION = 'v0.4.4'
AEON2_EXT = '.aeonzip'
PROPERTY_MOONPHASE = 'Moon phase'


def run(filePath):
    """Extract JSON data from an .aeonzip file
    and add or update the "Moon phase" property. 
    Return a message beginning with the ERROR constant in case of error.
    """
    if filePath.endswith(AEON2_EXT):
        message, jsonData = open_timeline(filePath)
        if message.startswith(ERROR):
            return message
    else:
        return(f'{ERROR}File format not supported.')

    #--- Get the date definition.
    for tplRgp in jsonData['template']['rangeProperties']:
        if tplRgp['type'] == 'date':
            for tplRgpCalEra in tplRgp['calendar']['eras']:
                if tplRgpCalEra['name'] == 'AD':
                    tplDateGuid = tplRgp['guid']
                    break

    if tplDateGuid is None:
        return f'{ERROR}"AD" era is missing in the calendar.'

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

    # Create a backup file.
    copy2(filePath, f'{filePath}.bak')
    return save_timeline(jsonData, filePath)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=f'Aeon Timeline 2 Add/update moon phase at event start date {VERSION}',
        epilog='"Moon phase" event property: phase day (0 to 29, where 0=new moon, 15=full etc.)')
    parser.add_argument('sourcePath', metavar='Sourcefile',
                        help='The path of the .aeonzip file.')
    args = parser.parse_args()
    print(run(args.sourcePath))

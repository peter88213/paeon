#!/usr/bin/env python3
"""Aeon Timeline 2 Add/update moon phase at event start date.

Version @release

usage: aeon2moon.py [-h] Sourcefile

positional arguments:
  Sourcefile  The path of the .aeonzip file.

optional arguments:
  -h, --help  show this help message and exit
  
"Moon phase" event property: phase day (0 to 29, where 0=new moon, 15=full etc.)

Copyright (c) 2021 Peter Triesberger
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import argparse
from shutil import copy2

from datetime import datetime
from datetime import timedelta

from pywriter.pywriter_globals import ERROR
from pywaeon2.aeon2_fop import open_timeline
from pywaeon2.aeon2_fop import save_timeline
from pywaeon2.uid_helper import get_uid
from pywaeon.moonphase import get_moon_phase_plus

VERSION = 'v@release'
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

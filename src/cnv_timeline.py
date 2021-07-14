#!/usr/bin/env python3
"""Create a yWriter 7 project from a csv file exported
by Aeon Timeline 2. 

Version @release
Requires Python 3.7 or above

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/Paeon
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import argparse

from pywriter.ui.ui import Ui
from pywriter.ui.ui_cmd import UiCmd
from paeon.csv.csv_converter import CsvConverter

SUFFIX = ''


def run(sourcePath, silentMode=True):

    if silentMode:
        ui = Ui('')

    else:
        ui = UiCmd('csv timeline to yWriter converter @release')

    converter = CsvConverter()
    converter.ui = ui
    kwargs = {'suffix': SUFFIX}
    converter.run(sourcePath, **kwargs)
    ui.start()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='csv timeline to yWriter converter',
        epilog='')
    parser.add_argument('sourcePath', metavar='Sourcefile',
                        help='The path of the csv timeline file.')

    parser.add_argument('--silent',
                        action="store_true",
                        help='suppress error messages and the request to confirm overwriting')
    args = parser.parse_args()

    if args.silent:
        silentMode = True

    else:
        silentMode = False

    if os.path.isfile(args.sourcePath):
        sourcePath = args.sourcePath

    else:
        sourcePath = None

    run(sourcePath, silentMode)

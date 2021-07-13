#!/usr/bin/env python3
"""yWriter/csv timeline converter. 

Version @release

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
        ui = UiCmd('yWriter/csv timeline converter @release')

    converter = CsvConverter()
    converter.ui = ui
    kwargs = {'suffix': SUFFIX}
    converter.run(sourcePath, **kwargs)
    ui.start()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='yWriter/csv timeline converter',
        epilog='')
    parser.add_argument('sourcePath', metavar='Sourcefile',
                        help='The path of the tineline csv file or yWriter project file.')

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

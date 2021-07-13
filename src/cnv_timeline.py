#!/usr/bin/env python3
"""Create a yWriter project from an Aeon 2 csv timeline. 

Version @release

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/Paeon
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
SUFFIX = ''

import sys

from pywriter.ui.ui_tk import UiTk
from paeon.csv.csv_converter import CsvConverter


def run(sourcePath, suffix=''):
    ui = UiTk('yWriter import/export')
    converter = CsvConverter()
    converter.ui = ui
    kwargs = {'suffix': suffix}
    converter.run(sourcePath, **kwargs)
    ui.start()


if __name__ == '__main__':
    run(sys.argv[1], SUFFIX)

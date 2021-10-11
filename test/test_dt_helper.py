"""Unit tests for Aeon3 file operation

Part of the paeon project (https://github.com/peter88213/paeon)
Copyright (c) 2021 Peter Triesberger
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import unittest

from paeon.dt_helper import fix_iso_dt

TEST_DT = [
    ['BC 333-04-05', None],
    ['33-04-05', None],
    ['100-04-05 21:23:00', '0100-04-05 21:23:00'],
    ['1910-04-05 21:23:00', '1910-04-05 21:23:00'],
    ['1910-04-05', '1910-04-05 00:00:00'],
    ['1910-04 21:23:00', '1910-04-01 21:23:00'],
    ['1910', '1910-01-01 00:00:00'],
    ['1910', '1910-01-01 00:00:00'],
]


class NormalOperation(unittest.TestCase):
    """Operation under normal condition, i.e.:
    * Test data is present and readable 
    * test data integrity is o.k.
    """

    def test_fix(self):

        for dt in TEST_DT:
            self.assertEqual(fix_iso_dt(dt[0]), dt[1])

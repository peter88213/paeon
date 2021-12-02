"""Unit tests for json_timeline2/3
Part of the paeon project (https://github.com/peter88213/paeon)
Copyright (c) 2021 Peter Triesberger
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import unittest
import json_timeline3
from shutil import copyfile

TEST_PATH = os.getcwd() + '/../test'
TEST_DATA_PATH = TEST_PATH + '/data/'
TEST_EXEC_PATH = TEST_PATH + '/yw7/'

AEON3 = TEST_DATA_PATH + 'normal.aeon'
REF_JSON3 = TEST_DATA_PATH + 'extract_json/normal.aeon.json'
TEST_AEON3 = TEST_EXEC_PATH + 'project.aeon'
TEST_JSON3 = TEST_EXEC_PATH + 'project.aeon.json'


def read_file(inputFile):

    try:
        with open(inputFile, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        with open(inputFile, 'r') as f:
            return f.read()


class NormalOperation(unittest.TestCase):
    """Operation under normal condition, i.e.:
    * Test data is present and readable 
    * test data integrity is o.k.
    """

    def tearDown(self):

        try:
            os.remove(TEST_AEON3)
        except:
            pass

        try:
            os.remove(TEST_JSON3)
        except:
            pass

    def test_aeon3(self):
        copyfile(AEON3, TEST_AEON3)
        timeline = JsonTimeline3(TEST_AEON3)
        self.assertEqual()


def main():
    unittest.main()


if __name__ == '__main__':
    main()

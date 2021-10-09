"""Unit tests for Aeon3 file operation

Part of the paeon project (https://github.com/peter88213/paeon)
Copyright (c) 2021 Peter Triesberger
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import unittest
import os
import json
import stat
from shutil import copyfile

from paeon.aeon3_fop import scan_file

TEST_DATA_REF = 'data/normal.aeon'
TEST_JSON_REF = 'data/fop/normal.json'
TEST_DATA = 'yw7/project.aeon'
TEST_JSON = 'yw7/project.aeon.json'


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

    def setUp(self):
        """Create an example project file by copying a reference file.
        """
        copyfile(TEST_DATA_REF, TEST_DATA)

    def tearDown(self):

        try:
            os.remove(TEST_DATA)
        except:
            pass

        try:
            os.remove(TEST_JSON)
        except:
            pass

    def test_scan(self):
        """Read the data from the example project file,
        """
        result = scan_file(TEST_DATA)
        self.assertEqual(read_file(TEST_JSON), read_file(TEST_JSON_REF))
        self.assertEqual(result, read_file(TEST_JSON_REF))


class CorruptedData(unittest.TestCase):
    """Operation under error condition, i.e.:
    * Test data is corrupted 
    """

    def setUp(self):
        """Create an example project file with corrupted data.
        """
        corruptedContent = 'abcdefg{123'

        with open(TEST_DATA, 'w') as f:
            f.write(corruptedContent)

    def tearDown(self):

        try:
            os.remove(TEST_DATA)
        except:
            pass
        try:
            os.remove(TEST_JSON)
        except:
            pass

    def test_read(self):
        """Read the data from the example project file.
        Expected result: program abort with error message.
        """
        message = scan_file(TEST_DATA)
        self.assertEqual(message, '')


class FileAccessError(unittest.TestCase):
    """Operation under error condition, i.e.:
    * Try to read a non-existent file
    * Try to overwrite a read-only file 
    """

    def setUp(self):
        """Create an example project file by copying a reference file.
        """
        copyfile(TEST_DATA_REF, TEST_DATA)

    def tearDown(self):

        try:
            os.chmod(TEST_DATA, stat.S_IWUSR | stat.S_IREAD)
            # Make the file writeable, if necessary
            os.remove(TEST_DATA)
        except:
            pass
        try:
            os.remove(TEST_JSON)
        except:
            pass

    def test_read(self):
        """Read the data from the example project file.
        Expected result: program abort with error message.
        """
        self.tearDown()
        # Make sure that the test file doesn't exist

        message = scan_file(TEST_DATA)
        self.assertEqual(message, 'ERROR: "' + os.path.normpath(TEST_DATA) + '" not found.')

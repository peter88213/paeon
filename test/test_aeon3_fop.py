"""Unit tests for Aeon3 file operation

Copyright (c) 2021 Peter Triesberger
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import unittest
import os
import stat

from paeon.aeon.aeon3_fop import read_aeon3, write_aeon3

TEST_DATA_REF = 'data/fop/normal.aeon'
TEST_DATA = 'workdir/project.aeon'


def read_file(inputFile):
    with open(inputFile, 'r') as f:
        return f.read()


def copy_file(inputFile, outputFile):
    with open(inputFile, 'rb') as f:
        myData = f.read()
    with open(outputFile, 'wb') as f:
        f.write(myData)
    return()


class NormalOperation(unittest.TestCase):
    """Operation under normal condition, i.e.:
    * Test data is present and readable 
    * test data integrity is o.k.
    """

    def setUp(self):
        """Create an example project file by copying a reference file.
        """
        copy_file(TEST_DATA_REF, TEST_DATA)

    def tearDown(self):

        try:
            os.remove(TEST_DATA)
        except:
            pass

    def test_read_write(self):
        """Read the data from the example project file,
        delete the example file and create a new one.
        The written file must match the reference file.
        """
        message, part1, part2, part3 = read_aeon3(TEST_DATA)
        self.assertEqual(message, 'SUCCESS: "' + TEST_DATA + '" read.')
        os.remove(TEST_DATA)
        message = write_aeon3(TEST_DATA, part1, part2, part3)
        self.assertEqual(message, 'SUCCESS: "' + TEST_DATA + '" written.')
        self.assertEqual(read_file(TEST_DATA), read_file(TEST_DATA_REF))


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

    def test_read(self):
        """Read the data from the example project file.
        Expected result: program abort with error message.
        """
        message, part1, part2, part3 = read_aeon3(TEST_DATA)
        self.assertEqual(message, 'ERROR: No JSON part found.')
        self.assertIsNone(part1)
        self.assertIsNone(part2)
        self.assertIsNone(part3)

    def test_write(self):
        """Try to create a project file with incomplete data.
        Expected result: program abort with error message.
        No file written.
        """
        self.tearDown()
        part1 = 'abc'
        part2 = None
        part3 = 'def'
        message = write_aeon3(TEST_DATA, part1, part2, part3)
        self.assertEqual(message, 'ERROR: Cannot assemble project parts.')
        self.assertFalse(os.path.isfile(TEST_DATA))


class FileAccessError(unittest.TestCase):
    """Operation under error condition, i.e.:
    * Try to read a non-existent file
    * Try to overwrite a read-only file 
    """

    def setUp(self):
        """Create an example project file by copying a reference file.
        """
        copy_file(TEST_DATA_REF, TEST_DATA)

    def tearDown(self):

        try:
            os.chmod(TEST_DATA, stat.S_IWUSR | stat.S_IREAD)
            # Make the file writeable, if necessary
            os.remove(TEST_DATA)
        except:
            pass

    def test_read(self):
        """Read the data from the example project file.
        Expected result: program abort with error message.
        """
        self.tearDown()
        # Make sure that the test file doesn't exist

        message, part1, part2, part3 = read_aeon3(TEST_DATA)
        self.assertEqual(message, 'ERROR: Cannot read "' + TEST_DATA + '".')
        self.assertIsNone(part1)
        self.assertIsNone(part2)
        self.assertIsNone(part3)

    def test_write(self):
        """Try to overwrite a read-only file.
        Expected result: program abort with error message.
        """
        message, part1, part2, part3 = read_aeon3(TEST_DATA)
        self.assertEqual(message, 'SUCCESS: "' + TEST_DATA + '" read.')
        # First read the data

        os.chmod(TEST_DATA, stat.S_IREAD)
        # Make the test file read-only

        message = write_aeon3(TEST_DATA, part1, part2, part3)
        self.assertEqual(message, 'ERROR: Can not write "' + TEST_DATA + '".')

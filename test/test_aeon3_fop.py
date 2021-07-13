"""Unit tests for Aeon3 file operation

Part of the paeon project (https://github.com/peter88213/paeon)
Copyright (c) 2021 Peter Triesberger
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import unittest
import os
import stat

from paeon.aeon.aeon3_fop import split_aeon3, join_aeon3

TEST_DATA_REF = 'data/normal.aeon'
TEST_BIN1_REF = 'data/fop/normal.bin1'
TEST_JSON_REF = 'data/fop/normal.json'
TEST_BIN2_REF = 'data/fop/normal.bin2'
TEST_DATA = 'workdir/project.aeon'
TEST_BIN1 = 'workdir/project.bin1'
TEST_JSON = 'workdir/project.json'
TEST_BIN2 = 'workdir/project.bin2'


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
        try:
            os.remove(TEST_BIN1)
        except:
            pass

        try:
            os.remove(TEST_JSON)
        except:
            pass

        try:
            os.remove(TEST_BIN2)
        except:
            pass

    def test_read_write(self):
        """Read the data from the example project file,
        delete the example file and create a new one.
        The written file must match the reference file.
        """
        message = split_aeon3(TEST_DATA, TEST_BIN1, TEST_JSON, TEST_BIN2)
        self.assertEqual(message, 'SUCCESS: Split files written.')
        self.assertEqual(read_file(TEST_BIN1), read_file(TEST_BIN1_REF))
        self.assertEqual(read_file(TEST_JSON), read_file(TEST_JSON_REF))
        self.assertEqual(read_file(TEST_BIN2), read_file(TEST_BIN2_REF))
        os.remove(TEST_DATA)
        message = join_aeon3(TEST_DATA, TEST_BIN1, TEST_JSON, TEST_BIN2)
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
        try:
            os.remove(TEST_JSON)
        except:
            pass

    def test_read(self):
        """Read the data from the example project file.
        Expected result: program abort with error message.
        """
        message = split_aeon3(TEST_DATA, TEST_BIN1, TEST_JSON, TEST_BIN2)
        self.assertEqual(message, 'ERROR: No JSON part found.')

    @unittest.skip("no realistic test scenario")
    def test_write(self):
        """Try to create a project file with incomplete data.
        Expected result: program abort with error message.
        No file written.
        """
        message = join_aeon3(TEST_DATA, TEST_BIN1, TEST_JSON, TEST_BIN2)
        self.assertEqual(message, 'ERROR: Cannot assemble the project.')
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

        message = split_aeon3(TEST_DATA, TEST_BIN1, TEST_JSON, TEST_BIN2)
        self.assertEqual(message, 'ERROR: Cannot read "' + TEST_DATA + '".')

    def test_write(self):
        """Try to overwrite a read-only file.
        Expected result: program abort with error message.
        """
        message = split_aeon3(TEST_DATA, TEST_BIN1, TEST_JSON, TEST_BIN2)
        self.assertEqual(message, 'SUCCESS: Split files written.')
        # First read the data

        os.chmod(TEST_DATA, stat.S_IREAD)
        # Make the test file read-only

        message = join_aeon3(TEST_DATA, TEST_BIN1, TEST_JSON, TEST_BIN2)
        self.assertEqual(message, 'ERROR: Can not write "' + TEST_DATA + '".')

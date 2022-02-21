""" Build a python script.
        
In order to distribute a single script without dependencies, 
this script "inlines" all modules imported from the.pyriter package.

For further information see https://github.com/peter88213/yw2html
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import sys 
sys.path.insert(0, f'{os.getcwd()}/../../PyWriter/src')
import inliner

SRC = '../src/'
BUILD = '../test/'
SOURCE_FILE = f'{SRC}extract_json_.py'
TARGET_FILE = f'{BUILD}extract_json.py'


def main():
    inliner.run(SOURCE_FILE, TARGET_FILE, 'aeon2ywlib', '../../aeon2yw/src/')
    inliner.run(TARGET_FILE, TARGET_FILE, 'aeon3ywlib', '../../aeon3yw/src/')
    print('Done.')


if __name__ == '__main__':
    main()

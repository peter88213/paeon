""" Build a python script.
        
In order to distribute a single script without dependencies, 
this script "inlines" all modules imported from the.pyriter package.

For further information see https://github.com/peter88213/yw2html
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import inliner

SRC = '../src/'
BUILD = '../test/'
SOURCE_FILE = 'aeon2moon_.py'
TARGET_FILE = BUILD + 'aeon2moon.py'


def main():
    os.chdir(SRC)

    try:
        os.remove(TARGET_FILE)

    except:
        pass

    inliner.run(SOURCE_FILE, TARGET_FILE, 'pywaeon2', '../../aeon2yw/src/')
    inliner.run(TARGET_FILE, TARGET_FILE, 'pywaeon', '../src/')
    print('Done.')


if __name__ == '__main__':
    main()

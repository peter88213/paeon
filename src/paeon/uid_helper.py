"""Provide a GUID generator for Aeon Timeline.
"""
import random

guidChars = list('ABCDEF0123456789')


def get_substring(size):
    """Return a randomized pseudo-hash.
    """
    return ''.join(random.choice(guidChars) for _ in range(size))


def get_uid():
    """Return a random GUID for Aeon Timeline.

    Form: aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee
    """
    sizes = [8, 4, 4, 4, 12]
    guid = []

    for size in sizes:
        guid.append(get_substring(size))

    return '-'.join(guid)

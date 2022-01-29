#!/usr/bin/env python3
"""Pretty print a JSON file
input file : command line parameter
output file : name of the input file with '.json' appended.
"""
import sys
import json

filename = sys.argv[1]

with open(filename, 'r', encoding='utf-8') as f:
    parsed = json.load(f)

with open(f'{filename}.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(parsed, indent=4, sort_keys=True))

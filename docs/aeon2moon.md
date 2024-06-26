[Project homepage](index) > aeon2moon

------------------------------------------------------------------

# aeon2moon.py

Aeon Timeline 2 - Add/update moon phase at event start date (only valid for the 20th and 21st centuries).

![Screenshot](Screenshots/moonphase01.png)

## Requirements

- [Python 3.6+](https://www.python.org). 

### Download:

- [aeon2moon_v0.5.0.zip (Download link)](https://raw.githubusercontent.com/peter88213/paeon/main/aeon2moon/dist/aeon2moon_v0.5.0.zip)

### Instructions for use:

### Intended usage

Unzip the Python script and create a shortcut on the desktop. 
- If you drag an *.aeonzip* file onto it and drop it, the event start moon phases are added or updated. 

### Command line usage

Alternatively, you can

- launch the program on the command line passing the *.aeonzip* file as an argument, or
- launch the program via a batch file.

usage: `aeon2moon.py [-h] Sourcefile`

positional arguments:
  `Sourcefile`  The path of the .aeonzip file.

optional arguments:
  `-h, --help`  show this help message and exit
  
"Moon phase" event property: phase day (0 to 29, where 0=new moon, 15=full etc.)


## Credits

- Ben Daglish published an [exemplary implementation](http://www.ben-daglish.net/moon.shtml) of John Conway's moon phase algorithm, though in JavaScript.

## License

aeon2moon.py is distributed under the [MIT License](http://www.opensource.org/licenses/mit-license.php).
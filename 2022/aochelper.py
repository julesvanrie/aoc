"""
Module with some helper functions for solving the Advent of Code puzzles.

- get_data(): Retrieves data from file or AOC website.
              Will behave based on the arguments passed to your python script.


Setup instructions:
==================
- Store this file somewhere on your computer.
- Add the path to the file's folder to your PYTHONPATH environment variable.
       `export PYTHONPATH=$PYTHONPATH:/path/to/the/file/folder`
       OR: add it to your ~/.zshrc file
- Create an environment variable with your Advent of Code website session cookie
  to allow the program to connect to your AOC challenges.
       `export AOC_SESSION=contents-of-the-session-cookie`


Usage instructions
==================
In your solution.py, add the following lines of code:

```
import sys
from aochelper import get_data

lines = get_data(sys.argv)
```

Now the lines variable contains your puzzle input.
"""

import os, requests
from datetime import datetime

def _read_file(filename):
    """
    Read lines from a text file called <filename> in the current directory.
    """
    with open(filename, "r") as fo:
        lines = [line.strip() for line in fo.readlines()]
    return lines

def _fetch_input(year, day):
    """
    Get the input from the Advent of Code website.
    Reads the session cookie from an environment variable called AOC_SESSION
    """
    session_cookie = os.getenv('AOC_SESSION')
    if not session_cookie:
        raise Exception("No session cookie stored in AOC_SESSION.\n" +
              "Please set the environment variable with your session cookie.\n")
    result = requests.get(
        f'https://adventofcode.com/{year}/day/{day}/input',
        cookies={'session': session_cookie}
    )
    if result.status_code != 200:
        raise Exception(f"GET request returned status code {result.status_code}.\n" +
              "Check if you provided a session cookie and it is still valid.\n" +
              "If that's not the cause, have fun debugging!\n")
    return result.text.strip().split('\n')

def get_data(sys_argv=[], year=None, day=None):
    """
    Gets the puzzle input data from a local file or from the AOC website.

    In your code, use `lines = get_data(sys.argv)` and it allows you to run
    your python script in the following ways to obtain the puzzle input:

    - python solution.py          >> get input for today's puzzle from the AOC website
    - python solution.py test     >> get input from test.txt
    - python solution.py 15       >> get input for day 15 from the AOC website
    - python solution.py 2021 15  >> get input for puzzle 15 of 2021

    Requires an environment variable 'AOC_SESSION' to be set to the value of
    your session cookie.

    More detailed instructions:
    ===========================

    If sys_argv has length 2, tries to convert the second arg to a day,
    otherwise reads the file with that name.txt.
    If sys_argv has length 3, converts the second and third arg to dates.
    Otherwise gets the input from the AOC date provided throug year and day.
    Defaults to current day and year if nothing else provided.
    """
    filename = None
    if len(sys_argv) == 2:
        try:
            day = int(sys_argv[1])
        except:
            filename = sys_argv[1]
    elif len(sys_argv) > 2:
        year = int(sys_argv[1])
        day = int(sys_argv[2])
    if filename:
        lines = _read_file(f"{filename}.txt")
        print('File', f"{filename}.txt", '------------------------------------')
    else:
        if not year:
            year = datetime.now().year
        if not day:
            day = datetime.now().day
        print(year, '- day',day, '------------------------------------')
        lines = _fetch_input(year, day)
    return lines

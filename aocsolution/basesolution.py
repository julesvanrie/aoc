import os, sys
import inspect
import requests
from datetime import datetime
import time

AOC_SESSION = os.environ['AOC_SESSION']


"""
Base Class for solving the Advent of Code puzzles.

- get_data(): Retrieves data from file or AOC website.
              Will behave based on the arguments passed to your python script.


Setup instructions:
==================
- pip install .
- Create an environment variable with your Advent of Code website session cookie
  to allow the program to connect to your AOC challenges.
       `export AOC_SESSION=contents-of-the-session-cookie`


Usage instructions
==================
Use the boilerplate.py to create a new solution.
Copy it for a new challenge.

You can now run your python script in the following ways
to obtain the puzzle input:
- python solve.py          >> if input.txt exists, read it
                                 else, get input for today's puzzle from
                                 the AOC website and save to input.txt
- python solve.py test     >> get input from test.txt
- python solve.py 15       >> get input for day 15 from the AOC website
- python solve.py 2021 15  >> get input for puzzle 15 of 2021
"""


class BaseSolution():

    def __init__(self, year=None, day=None, test=False):
        self.year = year if year else datetime.now().year
        self.day = day if day else datetime.now().day
        self.test = test


    def get_data(self, split=True):
        """
        Gets the puzzle input data from a local file or from the AOC website.

        Requires an environment variable 'AOC_SESSION' to be set to the value of
        your session cookie.

        If split is True: returns a list of lines
        If split is False: returns one long string for custom splitting
        """
        if self.test:
            input_path = f"test_{inspect.stack()[1].function[-3:]}.txt"
        else:
            input_path = "input.txt"
        try: # To read from file
            self.__print('File', input_path)
            input = self._read_file(input_path)
        except: # Fetch today's puzzle from site and save file
            self.__print('Fetched ', self.year, '- day', self.day, 'and saved to', input_path)
            input = self._fetch_input(filename=input_path)

        if split:
            return input.split("\n")
        return input


    def _read_file(self, filename):
        """
        Read lines from a text file called <filename> in the current directory.
        """
        with open(filename, "r") as fo:
            text = fo.read()
        return text.strip('\n')


    def _fetch_input(self, filename=None):
        """
        Get the input from the Advent of Code website.
        Reads the session cookie from an environment variable called AOC_SESSION
        """
        session_cookie = os.getenv('AOC_SESSION')
        if not session_cookie:
            raise Exception("No session cookie stored in AOC_SESSION.\n" +
                "Please set the environment variable with your session cookie.\n")
        result = requests.get(
            f'https://adventofcode.com/{self.year}/day/{self.day}/input',
            cookies={'session': session_cookie}
        )
        if result.status_code != 200:
            raise Exception(f"GET request returned status code {result.status_code}.\n" +
                "Check if you provided a session cookie and it is still valid.\n" +
                "If that's not the cause, have fun debugging!\n")

        if filename:
            with open(filename, "w") as fo:
                fo.writelines(result.text)

        return result.text.strip('\n')


    def time(self):
        with open(os.devnull, 'w') as out:
            sys.stdout = out
            number = 20
            timing = timeit.timeit(solve, number=number) / number
            sys.stdout = sys.__stdout__
        print(f"This took {timing:.6f} seconds")



    def __print(self, *args):
        print(*args)
        print("-------------------------------------")


    @classmethod
    def time_this(cls, func):
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            print(f"This took {(end-start) // 60} minutes, {round((end - start) % 60, 2)} seconds")
            return result
        return wrapper

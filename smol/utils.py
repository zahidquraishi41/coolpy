'''Miscellaneous utility functions and classes.'''

import time
import os
from sys import platform
from random import randint
from typing import List, Hashable, Any


def clear_screen() -> None:
    '''Clears the console.'''
    if platform in ('linux', 'linux2', 'darwin'):
        os.system('clear')
    elif platform == "win32":
        os.system('cls')


def display(msg: str, delay: float = 1.7) -> None:
    '''Displays a message and delays for specified time.

    ### Parameters
    @msg: message to be displayed.
    @delay: amount of time in seconds to delay for.
    '''
    print(msg)
    time.sleep(delay)


def pause():
    '''Waits for user to press enter key.'''
    input('Press enter to continue')


def get_key(d: dict, val: Any) -> Hashable:
    '''Retuns the first key that matches val.

    ### Raises
    KeyError if value if not found'''
    for k, v in d.items():
        if v == val:
            return k
    raise KeyError


def get_keys(d: dict, val: Any) -> List[Hashable]:
    '''Returns all keys that has value of val.'''
    keys = []
    for k, v in d.items():
        if v == val:
            keys.append(k)
    return keys


def random_list(size: int, min_val: int = 0, max_val: int = 1000) -> List[int]:
    '''Generates a random list of integers.

    ### Parameters
    @size: size of random list.
    @min_val: minimum value for each number.
    @max_val: maximum value for each number.

    ### Returns
    list containing random numbers.
    '''
    return [randint(min_val, max_val) for _ in range(size)]


def find(key: Any, l: list, ignore_case: bool = True):
    '''Searches for @key in @l, if it is found then returns it's index, Otherwise returns -1.'''
    if ignore_case:
        key = key.lower()
    for i, e in enumerate(l):
        if ignore_case:
            if e.lower() == key:
                return i
    return -1

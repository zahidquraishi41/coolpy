'''A simple Python menu-based UI system for terminal applications.'''

from .utils import clear_screen, display, find
from typing import Tuple, List


def choose(options: Tuple[str], msg: str = 'Enter your choice: ', header: str = None,
           commands: Tuple[str] = ()) -> str:
    '''Persistently asks user to choose an option from given list.

    ### Parameters
    @options: list of values that user have to choose from.
    @msg: will be passed to python's input().
    @commands: these are not displayed but if user enters them then it'll be returned.
    @header: if provided then it will be displayed before options.

    ### Returns
    Returns the option that was selected.
    '''
    clear_screen()
    size = len(options)

    if header:
        print(header)
    for i, option in enumerate(options):
        print(f'[{i + 1}] {option}')
    choice = input(msg)

    if choice in commands:
        return choice
    if not choice.isdigit():
        display(f'Enter a number between 1 and {size}')
        return choose(options, msg, header)
    choice = int(choice)
    if choice < 1 or choice > size:
        display(f'Enter a number between 1 and {size}')
        return choose(options, msg, header)

    return options[choice - 1]


def select(options: Tuple[str], msg: str = 'Enter your choice: ', header: str = None,
           commands: Tuple[str] = (), default_selections: Tuple[str] = (),
           min_selection: int = 1, max_selection: int = -1) -> List[str]:
    '''Persistently asks user to select one or more option from given list.

    ### Parameters
    @options: list of values that user have to choose from.
    @msg: will be passed to python's input().
    @commands: these are not displayed but if user enters them then it'll be returned.
    @header: if provided then it will be displayed before options.
    @default_selections: these options will be selected by default.
    @min_selection: minimum number of selections required.
    @max_selection: maximum number of selections that can be made. default -1 for all.

    ### Returns
    Returns list of options that were selected.
    '''
    choices = []
    choices.extend(default_selections)
    if max_selection == -1:
        max_selection = len(options)

    def is_selected(option: str):
        return 'Selected' if option in choices else 'Not Selected'

    def get_spacing(options: str):
        str_options = list(map(str, options))
        spacing = []
        max_chars = len(max(str_options, key=len))
        for option in str_options:
            spacing.append(max_chars - len(option))
        return spacing

    spacing = get_spacing(options)
    while True:
        clear_screen()
        size = len(options)

        if header:
            print(header)
        for i, option in enumerate(options):
            print(f'[{i + 1}] {option} {" " * spacing[i]} [{is_selected(option)}]')
        print()
        print(f'[a] Select All')
        print(f'[b] Select None')
        print(f'[c] Continue')
        choice = input(msg)

        if choice == 'a':
            i = 0
            while len(choices) < min(max_selection, len(options)):
                if options[i] not in choices:
                    choices.append(options[i])
                i += 1
            continue
        if choice == 'b':
            choices.clear()
            continue
        if choice == 'c':
            if len(choices) < min_selection:
                display(
                    f'You have to select at least {min_selection} to continue.')
                continue
            break
        if choice in commands:
            return choice
        if not choice.isdigit():
            display(f'Enter a number between 1 and {size}')
            continue
        choice = int(choice)
        if choice < 1 or choice > size:
            display(f'Enter a number between 1 and {size}')
            continue

        choice = options[choice - 1]
        if choice not in choices and len(choices) == max_selection:
            display(f'You can\'t select more than {len(choices)} options')
            continue
        if choice in choices:
            choices.remove(choice)
        else:
            choices.append(choice)

    return choices


def confirm(msg: str = 'Do you want to continue?', options: Tuple[str] = ('Y', 'N'), commands: Tuple[str] = (), ignore_case: bool = True) -> str:
    '''Persistently asks user to enter one of the option from given list.
    ### Parameters
    @options: list of values that user have to choose from.
    @msg: will be passed to python's input().
    @commands: these are not displayed but if user enters them then it'll be returned.'''
    while True:
        choice = input(f'''{msg} [{', '.join(options)}]: ''')
        index = find(choice, commands, ignore_case)
        if index != -1:
            return commands[index]
        index = find(choice, options, ignore_case)
        if index != -1:
            return options[index]

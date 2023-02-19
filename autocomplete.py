import readline
from typing import List, Any, Iterable
import os

''' Autocompleter
Provides easy interface to enable/disable autocompletion in terminal.
'''

class _Utils:
    @staticmethod
    def tree_to_str(option: Iterable, curr: str = '') -> List[str]:
        '''Traverse given tree and converts each path to string.

        ### Usage 1: Works with both list and tuple
        l = ['add', 'remove', ['update', 'delete']]
        tree_to_str(l)
        out: ['add', 'delete', 'remove', 'update']

        ### Usage 2: As long as value is false it'll be ignored
        d = {'add': None, 'remove': '', 'update': False, 'delete': []}
        tree_to_str(l)
        out: ['add', 'delete', 'remove', 'update']

        ### Usage 3
        ld = [{'add': 'filename'}, ['remove', 'update'], {'delete': {'all': None, 'random': False}}]
        tree_to_str(l)
        out: ['add filename', 'delete all', 'delete random', 'remove', 'update']

        ### Usage 4
        dl = {
            'pip': ['install', 'uninstall'],
            'shutdown': 'now',
        }
        tree_to_str(l)
        out: ['pip install', 'pip uninstall', 'shutdown now']
        '''
        lines = []
        space = ' ' if curr else ''

        if isinstance(option, str) or isinstance(option, int):
            lines.append(f'{curr}{space}{option}')

        elif isinstance(option, list) or isinstance(option, tuple):
            for e in option:
                if isinstance(e, str):
                    lines.append(f'{curr}{space}{e}')
                else:
                    lines.extend(_Utils.tree_to_str(e, curr))

        elif isinstance(option, dict):
            for k, v in option.items():
                if not v:
                    lines.append(curr + space + k)
                elif isinstance(v, str) or isinstance(v, int):
                    lines.append(f'{curr}{space}{k} {v}')
                else:
                    lines.extend(_Utils.tree_to_str(v, curr + space + k))

        return sorted(lines)

    @staticmethod
    def list_files() -> List[str]:
        files = []
        cwd = os.getcwd()
        for file in os.listdir():
            path = os.path.join(cwd, file)
            if os.path.isfile(path):
                files.append(path)
        return files

    @staticmethod
    def list_dirs() -> List[str]:
        dirs = []
        cwd = os.getcwd()
        for file in os.listdir():
            path = os.path.join(cwd, file)
            if os.path.isdir(path):
                dirs.append(path)
        return dirs


class AutoComplete:
    def __init__(self, option: Any = None) -> None:
        self.option = option
        self._enabled = False
        self._candidates = []
        self._shortlisted = []
        self._sr = ''

    def enable(self) -> None:
        # Register our completer function
        readline.set_completer(self.complete)
        readline.parse_and_bind('tab: complete')
        self._enabled = True

    def disable(self):
        readline.set_completer(lambda *_: None)
        readline.parse_and_bind('tab: \t')
        self._enabled = False

    def toggle(self):
        self.disable() if self._enabled else self.enable()

    def complete(self, text, state):
        '''Used by python's input().'''
        line = readline.get_line_buffer()
        if state == 0:
            # This is the first iteration for this text, so build a match list.
            candidates = _Utils.tree_to_str(self.option)
            shortlisted = []
            for candidate in candidates:
                if candidate.startswith(line):
                    shortlisted.append(candidate[len(line):].split()[0])
            self._sr = ' ' if candidate[len(line):].startswith(' ') else ''
            self._candidates = sorted(list(set(shortlisted)))

        try:
            out = self._candidates[state]
            out = None if out == line else out
            if len(self._candidates) == 1:
                return text + self._sr + out
            return out
        except:
            return None


if __name__ == '__main__':
    dl = {
        'pip': ['install', 'uninstall'],
        'shutdown': 'now'
    }
    ac = AutoComplete(dl)

    ac.enable()
    print('Autocomplete is enabled.')
    input('>>: ')

    ac.disable()
    print('Autocomplete is disabled.')
    input('>>: ')

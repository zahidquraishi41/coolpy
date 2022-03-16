from filecmp import cmp
import os
from os.path import join
from typing import List
from sys import platform
from time import time_ns


def clear_screen():
    if platform.startswith('win'):
        os.system('cls')
    else:
        os.system('clear')


def print_diplicates(paths: List[str]):
    files = []
    for root in paths:
        for path, _, names in os.walk(root):
            for name in names:
                file = join(path, name)
                files.append(file)

    size = len(files)
    similar_groups = []
    print(f'found: {size} file(s)')

    for i in range(size):
        print(f'\rProgress: {round(100*(i+1)/size, 1)}%', end='')
        if any([files[i] in groups for groups in similar_groups]):
            continue
        similars = []
        for j in range(i+1, size):
            is_similar = cmp(files[i], files[j], shallow=False)
            if is_similar:
                similars.append(files[j])
        if similars:
            similars.insert(0, files[i])
            similar_groups.append(similars)

    dups = sum([len(groups) for groups in similar_groups]) \
        - len(similar_groups)
    print(f'\nfound {len(similar_groups)} group(s) & {dups} duplicate(s).\n')

    if len(similar_groups) > 15:
        return similar_groups

    for i, group in enumerate(similar_groups):
        print(f'[Group {i+1}]')
        print('\n'.join(group))
        print()

    return similar_groups


def validate_path(path: str):
    if not os.path.exists(path):
        print('Given path does not exists.')
        return
    if os.path.isfile(path):
        print('Enter a directory path.')
        return

    return True


def print_help():
    print('Enter /list to list all paths that are added.')
    print('Enter /continue to start searching.')
    print('Enter /help to display this help.')
    print('Enter /remove PATH to remove path from list.')
    print('Enter /clear to clear screen.')
    print('Enter /exit to exit.')


def input_paths() -> List[str]:
    clear_screen()
    print_help()
    paths = []
    while True:
        print()
        command = input('Enter path: ')
        if command == '/list':
            if not paths:
                print('No path added.')
            else:
                print('\n'.join(paths))

        elif command == '/continue':
            if not paths:
                print('Add at least one path to continue.')
            else:
                break

        elif command == '/help':
            print_help()

        elif command == '/exit':
            exit(0)

        elif command == '/clear':
            clear_screen()

        elif command.startswith('/remove '):
            path = command.split(' ', 1)[1]
            if path in paths:
                paths.remove(path)
                print('Removed successfully.')
            else:
                print(f'"{path}" is not added.')

        else:
            if validate_path(command):
                if command in paths:
                    print('Path is already added.')
                    continue
                for path in paths:
                    if command.startswith(path):
                        print(
                            f'"{command}" is replaced with parent directory "{path}"')
                        paths.remove(path)
                        paths.append(command)
                        break
                    elif path.startswith(command):
                        print(
                            f'"{path}" is replaced with parent directory "{command}"')
                        paths.remove(path)
                        paths.append(command)
                        break
                else:
                    paths.append(command)
                    print('Added successfully.')

    return paths


def safe_delete(similar_groups: List[List[str]]):
    count = 0
    for groups in similar_groups:
        for file in groups[1:]:
            os.remove(file)
            print(f'Removed: {file}')
            count += 1
    print(f'Removed: {count} file(s)')


def create_log(similar_groups: List[List[str]]):
    with open(f'log_{time_ns()}.txt', 'w') as f:
        for i, group in enumerate(similar_groups):
            f.write(f'[Group {i+1}]\n')
            f.write('\n'.join(group))
            f.write('\n\n')


if __name__ == '__main__':
    paths = input_paths()
    groups = print_diplicates(paths)
    if len(groups) == 0:
        exit(0)
    choice = input('Create log? (y/n): ')
    if choice in ('y', 'Y'):
        create_log(groups)
    choice = input('Safely remove duplicates: (y/n): ')
    if choice in ('y', 'Y'):
        safe_delete(groups)

import argparse
from collections import defaultdict
from itertools import permutations
import os
from typing import Dict, Set, List


def load_words(file_path) -> Set[str]:
    with open(file_path, 'r') as file:
        words = file.read().splitlines()
    return set(words)


def find_anagrams(letters, dictionary) -> Dict[int, List[str]]:
    anagrams = defaultdict(list)
    n = len(letters)
    for length in range(3, n + 1):
        words = []
        for perm in permutations(letters, length):
            candidate = ''.join(perm)
            if candidate in dictionary:
                words.append(candidate)
        if words:
            anagrams[length] = sorted(set(words))
    return anagrams


def main():
    parser = argparse.ArgumentParser(description='Find anagrams from a given set of letters.')
    parser.add_argument('letters', type=str, nargs='?', help='The input letters for generating anagrams')
    parser.add_argument('--file', type=str, default='dictionary.txt', help='Path to the file containing valid words')

    args = parser.parse_args()
    dict_path = args.file
    letters = args.letters
    
    if not os.path.exists(dict_path):
        print(f"Error: The file '{dict_path}' was not found.")
        exit(1)
    elif os.path.isdir(dict_path):
        print(f"Error: The path '{dict_path}' is not a valid file.")
        exit(1)    
    
    if letters is None:
        letters = input('Enter the letters: ')
    letters = letters.strip().lower()
    if len(letters) < 3:
        print(f'Error: Input must contain at least 3 letters.')
        exit(1)


    dictionary = load_words(dict_path)
    anagrams = find_anagrams(letters, dictionary)
    for k, v in anagrams.items():
        print(f'{k} Letter Words:')
        print(' '.join(v))
        print()


if __name__ == '__main__':
    main()

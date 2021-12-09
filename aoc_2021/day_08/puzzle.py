from typing import Tuple, List, Dict

from aoc_2021.day_08.input import puzzle_inputs

test_input = ["acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"]
display_mask = """
 0000
1    2
1    2
 3333
4    5
4    5
 6666"""


def parse_input(input_str: str) -> Tuple[List[str], List[str]]:
    patterns, digits = input_str.split(' | ')
    return patterns.split(' '), ["".join(sorted(digit for digit in digit_str)) for digit_str in digits.split(' ')]


NUMBERS = {
    0: "012456",
    1: "25",
    2: "02346",
    3: "02356",
    4: "1235",
    5: "01356",
    6: "013456",
    7: "025",
    8: "0123456",
    9: "012356"
}


def print_num(n: int):
    for line in display_mask:
        for char in line:
            if char == '\n':
                print('')
            elif char == ' ':
                print(char, end='')
            elif char in NUMBERS[n]:
                print('x', end='')
            else:
                print(' ', end='')
    print('')


def solve_one(patterns):
    patterns.sort(key=lambda x: len(x))

    permutation_lists: list[tuple[str, list[list[int]]]] = [
        (pattern, [[int(segment) for segment in segments]
                   for _, segments
                   in NUMBERS.items()
                   if len(segments) == len(pattern)
                   ])
        for pattern in patterns
    ]

    """
    [('eafb', [[1, 2, 3, 5]]), ('cdfbe', [[0, 2, 3, 4, 6], [0, 2, 3, 5, 6], [0, 1, 3, 5, 6]]), ...
    """

    def gen_permutations(perm_list: list[tuple[str, list[list[int]]]]):
        """
        [('ab', [2, 5]), ('dab', [0, 2, 5]), ('eafb', [1, 2, 3, 5]),
        """
        head, *tail = perm_list
        patt, digit_lists = head
        for digit_list in digit_lists:
            if not tail:
                yield [(patt, digit_list)]
            else:
                for rest in gen_permutations(tail):
                    yield [(patt, digit_list)] + rest

    # remove permutations where the same segment list appears twice
    filtered_permutations = (
        perm
        for perm
        in gen_permutations(permutation_lists)
        # there has to be as many distinct segment lists as the total number of elements in the permutation
        if len({"".join(str(s) for s in sorted(segment)) for _, segment in perm}) == len(permutation_lists)
    )

    def eliminate(permutations):
        for permutation in permutations:
            codes = {letter: list(range(7)) for letter in 'abcdefg'}
            for pattern, segments in permutation:
                for letter in pattern:
                    codes[letter] = [code for code in codes[letter] if code in segments]
            # if no pattern is without any possible segment is empty
            if not any(not segment_nums for _, segment_nums in codes.items()):
                # there is only one possible elimination return that one
                return [(letter, set(segments)) for letter, segments in codes.items()]

    # subtract shorter sets from longer sets
    pattern_to_segment_mapping = dict(sorted(eliminate(filtered_permutations), key=lambda x: len(x[1])))
    """
    [('a', {2}), ('b', {5}), ('d', {0}), ('f', {3}), ('c', {0, 6}), ('e', {1, 5}), ('g', {0, 4, 6})]
    ->
    {'a': {2}, 'b': {5}, 'd': {0}, 'f': {3}, 'c': {6}, 'e': {1}, 'g': {4}}
    """
    for pattern, segments in pattern_to_segment_mapping.items():
        for target_pattern, target_segments in pattern_to_segment_mapping.items():
            if pattern != target_pattern and \
                    len(segments) < len(target_segments):
                pattern_to_segment_mapping[target_pattern] = target_segments.difference(segments)
    # print(pattern_to_segment_mapping)

    """
    invert pattern_to_segment_mapping
    {2: 'a', 5: 'b', 0: 'd', 3: 'f', 6: 'c', 1: 'e', 4: 'g'}
    """
    segment_to_pattern_mapping = {
        segment.pop(): pattern
        for pattern, segment
        in pattern_to_segment_mapping.items()
        if len(segment) == 1
    }
    # print(segment_to_pattern_mapping)

    """
    translate NUMBERS with pattern_to_segment_mapping
    {'abcdeg': 0, 'ab': 1, 'acdfg': 2, 'abcdf': 3, 'abef': 4, 'bcdef': 5, 'bcdefg': 6, 'abd': 7, 'abcdefg': 8, 'abcdef': 9}
    """
    pattern_decoder = {
        "".join(sorted({segment_to_pattern_mapping.get(int(segment)) for segment in segments})): display_number
        for display_number, segments
        in NUMBERS.items()
    }
    # print(pattern_decoder)

    return pattern_decoder


if __name__ == '__main__':
    all_displayed_digits = []
    for line in puzzle_inputs:
        # for line in test_input:
        patterns, digits = parse_input(line)
        decoder_map = solve_one(patterns)
        # print(decoder_map)
        # print(digits)
        displayed_digits = [decoder_map.get(digit) for digit in digits]
        all_displayed_digits.append(displayed_digits)

    print('all displayed digits:', all_displayed_digits)

    looking_for = {1, 4, 7, 8}
    print(f'number of time the digits {looking_for} is displayed:',
          len([
              num
              for nums in all_displayed_digits
              for num in nums
              if num in looking_for
          ]))

    all_displayed_numbers = [
        int("".join(str(digit) for digit in digits))
        for digits
        in all_displayed_digits
    ]

    print('all displayed numbers:', all_displayed_numbers)
    print('sum of all displayed numbers:', sum(all_displayed_numbers))

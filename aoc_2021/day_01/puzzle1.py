from typing import List

from aoc_2021.day_01.input import puzzle_input

test_input = [
    199,
    200,
    208,
    210,
    200,
    207,
    240,
    269,
    260,
    263,
]


def count_larger_than_the_previous(depth_measurments: List[int]):
    """
    >>> test_input = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]
    >>> count_larger_than_the_previous(test_input)
    7
    """
    pairs = zip(depth_measurments[1:], depth_measurments)
    return sum(1 for this_depth, prev_depth in pairs if this_depth > prev_depth)


def count_larger_than_the_previous_windowed(depth_measurments: List[int]):
    """
    >>> test_input = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]
    >>> count_larger_than_the_previous_windowed(test_input)
    5
    """
    windows = [sum(tup)
               for tup
               in zip(depth_measurments[2:], depth_measurments[1:], depth_measurments)]
    return count_larger_than_the_previous(windows)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    # print(count_larger_than_the_previous(puzzle_input))
    print(count_larger_than_the_previous_windowed(puzzle_input))

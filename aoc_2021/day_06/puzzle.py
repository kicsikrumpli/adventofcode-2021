from collections import defaultdict
from itertools import groupby
from operator import itemgetter
from typing import List, Dict

from aoc_2021.day_06.input import puzzle_input

test_input = [3, 4, 3, 1, 2]


def input_to_dict(fish: List[int]) -> Dict[int, int]:
    return {cycle: len(list(count))
            for cycle, count
            in groupby(sorted(fish))}


def tick(fish: Dict[int, int]) -> Dict[int, int]:
    reduced_cycles = [
        (cycle - 1, count)
        for cycle, count
        in fish.items()
    ]
    new_breeds = [
        (8, count)
        for cycle, count
        in reduced_cycles
        if cycle == -1
    ]
    reset_cycles = [
        (cycle if cycle >= 0 else 6, count)
        for cycle, count
        in reduced_cycles
    ]
    return {
        cycle: sum(list(c for _, c in group))
        for cycle, group
        in groupby(sorted([*new_breeds, *reset_cycles], key=itemgetter(0)), itemgetter(0))
    }


def total_fish(fish: Dict[int, int]) -> int:
    return sum(count for count in fish.values())


if __name__ == '__main__':
    # fish = input_to_dict(fish=test_input)
    fish = input_to_dict(fish=puzzle_input)
    print(fish)
    # days = 18
    # days = 80
    days = 256
    for day in range(days):
        fish = tick(fish)
        print(f'{day} | [{total_fish(fish)}]: {fish}')
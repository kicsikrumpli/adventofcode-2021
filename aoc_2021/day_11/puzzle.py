from itertools import count
from typing import List, Tuple

from aoc_2021.day_11.input import puzzle_input

test_input = [
    "5483143223",
    "2745854711",
    "5264556173",
    "6141336146",
    "6357385478",
    "4167524645",
    "2176841721",
    "6882881134",
    "4846848554",
    "5283751526",
]


def parse(octostr: List[str]) -> List[List[int]]:
    return [
        [int(n) for n in line]
        for line
        in octostr
    ]


def shape(flat_list: List[int], _shape: Tuple[int, int]) -> List[List[int]]:
    _width, _height = _shape
    return [
        flat_list[_width * h: _width * (h + 1)]
        for h
        in range(_height)
    ]


def flatten(mtx: List[List[int]]) -> List[int]:
    return [
        n
        for line in mtx
        for n in line
    ]


def display(octopi: List[int]):
    for line in shape(octopi, (10, 10)):
        for n in line:
            print(n if n > 0 else '*', end='')
        print('')


def step(octopi: List[int], width: int, height: int) -> List[int]:
    def _neighbors(idx: int):
        x_0, y_0 = idx % width, idx // height
        return [
            y * height + x
            for x in range(x_0 - 1, x_0 + 2)
            for y in range(y_0 - 1, y_0 + 2)
            if 0 <= x < width and 0 <= y < height
        ]

    def _step(_octopi: List[int], flash_indices: List[int]) -> List[int]:
        if not flash_indices:
            return _octopi
        else:
            flash_idx = flash_indices.pop()
            # increment flasher and its neighbors:
            neighbours = _neighbors(flash_idx)
            _octopi = [
                o + 1 if idx in neighbours else o
                for idx, o in enumerate(_octopi)
            ]
            # ones that just flashed?
            new_flash_indices = [idx for idx in neighbours if _octopi[idx] == 10]
            # print(new_flash_indices, flash_indices)
        return _step(_octopi, [*new_flash_indices, *flash_indices])

    incremented = [o + 1 for o in octopi]
    first_flash_indices = [idx for idx, o in enumerate(incremented) if o == 10]
    after_step = [
        o if o < 10 else 0
        for o
        in _step(incremented, first_flash_indices)
        ]
    return after_step


if __name__ == '__main__':
    # octopi = parse(test_input)
    octopi = parse(puzzle_input)

    width = len(octopi[0])
    height = len(octopi)

    o = flatten(octopi)

    iteration = 0
    is_in_sync = False
    no_of_flashes = 0
    while not is_in_sync or iteration < 100:
        iteration += 1
        o = step(o, width, height)
        # display(o)
        no_of_flashes += sum(1 for o in o if o == 0)
        is_in_sync = is_in_sync or all(octopus == 0 for octopus in o)
        if iteration == 100:
            print(f'number of flashes after {iteration} iterations: {no_of_flashes}')
        if is_in_sync:
            print(f'flashes sync after {iteration} iterations')

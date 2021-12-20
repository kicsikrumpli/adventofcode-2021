from itertools import count
from typing import Tuple, Callable, List

from aoc_2021.day_17.input import puzzle_input

test_input = "target area: x=20..30, y=-10..-5"


def parse(input_s: str) -> Tuple[int, int, int, int]:
    x_range, y_range = input_s \
        .replace('target area: ', '') \
        .replace('x=', '') \
        .replace('y=', '') \
        .split(', ')
    x_min, x_max = x_range.split('..')
    y_min, y_max = y_range.split('..')
    return int(x_min), int(x_max), int(y_min), int(y_max)


def step_x(x: int, v_x: int) -> Tuple[int, int]:
    x += v_x
    v_x = v_x - (abs(v_x) // v_x) if v_x else 0
    return x, v_x


def step_y(y: int, v_y: int) -> Tuple[int, int]:
    y += v_y
    v_y -= 1
    return y, v_y


def loop_y(start_v_y: int,
           y_min_limit: int) -> List[int]:

    start_y = 0

    def step_iterator():
        y = start_y
        v_y = start_v_y
        while y >= y_min_limit:
            y, v_y = step_y(y, v_y)
            yield y

    return [y for y in step_iterator()]
    # if any(y_min_limit < point < y_max_limit for point in points):
    #     return points
    # else:
    #     return []


def find_max_y(y_max_limit: int,
               y_min_limit: int) -> int:

    print(f'target y: {y_max_limit}..{y_min_limit}')
    apex = []
    for v_y in range(1000): # count():
        points = loop_y(v_y, y_min_limit)
        if any(y_min_limit <= point <= y_max_limit for point in points):
            print(points)
            apex.append(max(points))
        else:
            apex.append(-1)
            # break
    print('---')
    print(apex)
    return max(apex)


if __name__ == '__main__':
    # x_min, x_max, y_min, y_max = parse(test_input)
    x_min, x_max, y_min, y_max = parse(puzzle_input)
    max_apex = find_max_y(y_max, y_min)
    print('highest point:', max_apex)


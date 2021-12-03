from enum import Enum
from functools import reduce
from typing import Tuple, List, Generator, Optional

from aoc_2021.day_02.input import puzzle_input


class Directions(Enum):
    forward = 'forward'
    down = 'down'
    up = 'up'


test_input = [
    ('forward', 5),
    ('down', 5),
    ('forward', 8),
    ('up', 3),
    ('down', 8),
    ('forward', 2),
]


def move(pos: Optional[Tuple[int, int]], _input: Tuple[str, int]) -> Tuple[int, int]:
    """
    >>> move((0,0), ('forward', 5))
    (5, 0)

    >>> move((0, 0), ('up', 2))
    (0, -2)

    >>> move((0, 0), ('down', 3))
    (0, 3)
    """
    vectors = {
        'forward': (1, 0),
        'down': (0, 1),
        'up': (0, -1),
    }
    if pos is None:
        pos = (0, 0)

    direction_name, magnitude = _input
    horiz, vert = vectors.get(direction_name)
    h_pos, v_pos = pos
    return h_pos + horiz * magnitude, v_pos + vert * magnitude


def move_with_aim(pos: Tuple[int, int, int], _input: Tuple[str, int]) -> Tuple[int, int, int]:
    """
    >>> move_with_aim((0, 0, 0), ('forward', 5))
    (0, 5, 0)
    >>> move_with_aim((0, 5, 0), ('down', 5))
    (5, 5, 0)
    >>> move_with_aim((5, 5, 0), ('forward', 8))
    (5, 13, 40)
    >>> move_with_aim((5, 13, 40), ('up', 3))
    (2, 13, 40)
    """
    vectors = {
        'forward': (0, 1),
        'down': (1, 0),
        'up': (-1, 0),
    }
    aim, h_pos, v_pos = pos
    direction_name, magnitude = _input
    v_aim, v_h_pos = vectors.get(direction_name)  # base vectors
    return aim + v_aim * magnitude, h_pos + v_h_pos * magnitude, v_pos + v_h_pos * aim * magnitude


def where_am_i(start: Tuple[int, int]) -> Generator[Tuple[str, int], None, None]:
    pos = start
    while True:
        next_move = yield pos
        if next_move is None:
            break
        pos = move(pos, next_move)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # end_pos = reduce(move, test_input, (0, 0))
    end_pos = reduce(move, puzzle_input, (0, 0))
    h, v = end_pos
    print(end_pos, h * v)

    # end_pos = reduce(move_with_aim, test_input, (0, 0, 0))
    end_pos = reduce(move_with_aim, puzzle_input, (0, 0, 0))
    _, h, v = end_pos
    print(end_pos, h * v)


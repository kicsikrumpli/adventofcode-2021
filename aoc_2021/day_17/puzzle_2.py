from typing import List, Callable, Tuple, Iterator

from aoc_2021.day_17.input import puzzle_input
from aoc_2021.day_17.puzzle import step_x, step_y, parse, test_input


def plot(t_range: Iterator[int],
         v_range: Iterator[int],
         step_fn: Callable[[int, int], Tuple[int, int]]) -> List[List[int]]:
    """
    v0
    |
    |    x -- distance at time t w/ initial velocity v0
    |
    +----------->t
    :return: v0 / t table:
    [
         t = 0 1 2 3 4 ...
    v0 = 0: [ ... dist(v0, t)    ]
    v0 = 1: [ ...                ]
    ...
    ]
    address as table[v0][t]
    """

    def step(v0: int, t: Iterator[int]):
        dist = 0
        v = v0
        for _ in t:
            yield dist
            dist, v = step_fn(dist, v)

    return [
        [dist for dist in step(v0, t_range)]
        for v0 in v_range
    ]


def eval_at_t_slice(table: list[list[int]],
                    t: int,
                    predicate: Callable[[int], bool]) -> list[bool]:
    """
    takes a vertical slice (t) from table,
    evaluates predicate for every element of slice
    """
    return [
        predicate(line[t])
        for line
        in table
    ]


if __name__ == '__main__':
    # x_min, x_max, y_min, y_max = parse(test_input)
    x_min, x_max, y_min, y_max = parse(puzzle_input)

    # make table for x, y separately
    # take slices from both tables at the same t values
    # count distances in target zone for x, and y coordinates at slice t -> x_t, y_t
    # number of original velocities at t = x_t * y_t
    # ??? how to not count the same combination twice? ie.:
    #   same vx - vy combination is in the target zone for multiple t values?
    # !!! put combinations in a set

    # what's the range? guess / increase until it does not change... duh!

    T_MAX = 400
    VX_MAX = 500
    VY_MIN = -500
    VY_MAX = 500
    horizontal_table = plot(t_range=range(T_MAX), v_range=range(VX_MAX), step_fn=step_x)
    vertical_table = plot(t_range=range(T_MAX), v_range=range(VY_MIN, VY_MAX), step_fn=step_y)

    combinations = {  # set b/c projectile may remain in target area for multiple t values
        (vx_0, vy_0 + VY_MIN)  # vy range: VY_MIN .. VY_MAX, not from 0
        for t in range(T_MAX)
        for vx_0, x_in_target in enumerate(eval_at_t_slice(
            table=horizontal_table,
            t=t,
            predicate=lambda x: x_min <= x <= x_max
        ))
        for vy_0, y_in_target in enumerate(eval_at_t_slice(
            table=vertical_table,
            t=t, predicate=lambda y: y_min <= y <= y_max
        ))
        if x_in_target and y_in_target
    }

    print(len(combinations))
    # 329 too low
    # 369 too low
    # 1566
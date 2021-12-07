from typing import List, Callable, Iterator

from aoc_2021.day_07.input import puzzle_input

test_input = [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]


def puzzle_1_cost_fn(submarine_position: int, target_position: int):
    return abs(submarine_position - target_position)


def puzzle_2_cost_fn(submarine_position: int, target_position: int):
    return sum(range(abs(submarine_position - target_position) + 1))


def total_fuel_costs(positions: List[int], cost_fn: Callable[[int, int], int]) -> Iterator[int]:
    return (
        sum([cost_fn(pos, x) for pos in positions])
        for x
        in range(min(positions), max(positions) + 1)
    )


if __name__ == '__main__':
    # fuel_costs = total_fuel_costs(test_input, puzzle_1_cost_fn)
    # fuel_costs = total_fuel_costs(puzzle_input, puzzle_1_cost_fn)
    # fuel_costs = total_fuel_costs(test_input, puzzle_2_cost_fn)
    fuel_costs = total_fuel_costs(puzzle_input, puzzle_2_cost_fn)
    print(min(fuel_costs))

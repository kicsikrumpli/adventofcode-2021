import operator
from functools import reduce
from typing import List, Optional, Tuple, Set

from aoc_2021.day_09.input import puzzle_input

test_input = [
    "2199943210",
    "3987894921",
    "9856789892",
    "8767896789",
    "9899965678",
]


def low_points(height_map: List[str]) -> list[tuple[tuple[int, int], int]]:
    width = len(height_map[0])
    height = len(height_map)
    low_point_map = [
        ((x, y), int(point))
        for y, line in enumerate(height_map)
        for x, point in enumerate(line)
        if (point < height_map[y][x-1] if x - 1 >= 0 else True) and \
           (point < height_map[y][x + 1] if x + 1 < width else True) and \
           (point < height_map[y - 1][x] if y - 1 >= 0 else True) and \
           (point < height_map[y + 1][x] if y + 1 < height else True)
    ]
    return low_point_map


def flood_fill(x: int,
               y: int,
               height_map: List[str],
               visited: Optional[set] = None) -> Set[Tuple[int, int]]:
    width = len(height_map[0])
    height = len(height_map)
    if visited is None:
        visited = set()
    if (x, y) in visited:
        # been here
        return set()
    if x < 0 or x >= width or y < 0 or y >= height:
        # went off the map
        return set()

    point = height_map[y][x]
    if point == '9':
        # border
        return set()

    visited.add((x, y))
    left = flood_fill(x - 1, y, height_map, visited)
    right = flood_fill(x + 1, y, height_map, visited.union(left))
    up = flood_fill(x, y - 1, height_map, visited.union(left).union(right))
    down = flood_fill(x, y + 1, height_map, visited.union(left).union(right).union(up))

    return visited.union(left).union(right).union(up).union(down)


def risk_levels(low_point_map: list[tuple[tuple[int, int], int]]) -> int:
    risk_level_list = [point + 1 for _, point in low_point_map]
    return sum(risk_level_list)


if __name__ == '__main__':
    # height_map = test_input
    height_map = puzzle_input
    low_point_map = low_points(height_map)
    total_risk_level = risk_levels(low_point_map)
    print('sum of risk levels:', total_risk_level)
    print('-'*10)
    low_points = (
        (x, y)
        for (x, y), _ in low_point_map
    )
    basins = (
        flood_fill(x, y, height_map)
        for (x, y), _ in low_point_map
    )
    basin_sizes = (
        len(basin)
        for basin in basins
    )
    three_largest = sorted(basin_sizes, reverse=True)[0:3]
    print(three_largest)
    product_of_basin_sizes = reduce(operator.mul, three_largest)
    print('product_of_basin_sizes:', product_of_basin_sizes)

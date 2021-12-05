from itertools import groupby
from operator import itemgetter
from typing import Tuple, Dict, List

from aoc_2021.day_05.input import puzzle_input

test_input = [
    "0,9 -> 5,9",
    "8,0 -> 0,8",
    "9,4 -> 3,4",
    "2,2 -> 2,1",
    "7,0 -> 7,4",
    "6,4 -> 2,0",
    "0,9 -> 2,9",
    "3,4 -> 1,4",
    "0,0 -> 8,8",
    "5,5 -> 8,2",
]

Coord_2d = Tuple[int, int]


def parse_segment(line: str) -> List[int]:
    start, end = line.split(" -> ")
    return [int(x) for x in (*start.split(','), *end.split(','))]


def is_ortho(segment: List[int]) -> bool:
    start_x, start_y, end_x, end_y = segment
    return start_x == end_x or start_y == end_y


def points_of_segment(segment: List[int]) -> List[Tuple[Coord_2d, int]]:
    """horizontal, vertical, ±45° lines"""
    start_x, start_y, end_x, end_y = segment
    step = (end_x - start_x) // (abs(end_x - start_x) or 1), \
           (end_y - start_y) // (abs(end_y - start_y) or 1)
    if step == (0, 0):
        return [((end_x, end_y), 1)]
    else:
        step_x, step_y = step
        return [((start_x, start_y), 1), *points_of_segment([start_x + step_x, start_y + step_y, end_x, end_y])]


def merge_list_of_points(points: List[Tuple[Coord_2d, int]]) -> Dict[Coord_2d, int]:
    return dict(
        (point, len(list(grouper)))
        for point, grouper
        in groupby(sorted(points), itemgetter(0))
    )


def count_overlapping_points(points: Dict[Coord_2d, int]):
    return len([val for val in points.values() if val > 1])


if __name__ == '__main__':
    # segments = [parse_segment(line) for line in test_input]
    segments = [parse_segment(line) for line in puzzle_input]
    all_points = [
        points
        for segment in segments
        for points in points_of_segment(segment)
        # if is_ortho(segment)  # ortho lines only for puzzle 1
    ]
    merged_points = merge_list_of_points(all_points)
    print('number of overlapping points: ', count_overlapping_points(merged_points))

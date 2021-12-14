from itertools import groupby
from operator import itemgetter
from typing import Dict, List, Tuple, Callable

from aoc_2021.day_12.input import puzzle_input

test_input = [
    [
        "start-A",
        "start-b",
        "A-c",
        "A-b",
        "b-d",
        "A-end",
        "b-end",
    ], [
        "dc-end",
        "HN-start",
        "start-kj",
        "dc-start",
        "dc-HN",
        "LN-dc",
        "HN-end",
        "kj-sa",
        "kj-HN",
        "kj-dc",
    ], [
        "fs-end",
        "he-DX",
        "fs-he",
        "start-DX",
        "pj-DX",
        "end-zg",
        "zg-sl",
        "zg-pj",
        "pj-he",
        "RW-he",
        "fs-DX",
        "pj-RW",
        "zg-RW",
        "start-pj",
        "he-WI",
        "zg-he",
        "pj-fs",
        "start-RW",
    ]
]


def parse(edges: List[str]) -> Dict[str, List[str]]:
    graph = []
    for edge in edges:
        node_a, node_b = edge.split('-')
        graph.append((node_a, node_b))
        graph.append((node_b, node_a))

    return {
        key: sorted([end
                     for _, end
                     in values])
        for key, values
        in groupby(sorted(graph, key=itemgetter(0)), key=itemgetter(0))
    }


def next_cave_predicate_puzzle_1(cave: str, visited: List[str]) -> bool:
    """small caves can only be visited once"""
    return cave.isupper() or cave not in visited


def next_cave_predicate_puzzle_2(cave: str, visited: List[str]) -> bool:
    """
    one small cave can be visited twice, other small caves can be visited at most once
    start and end caves can only be visited once
    """
    def no_double_small_caves():
        small_caves = list(v for v in visited if v.islower())
        return len(small_caves) == len(set(small_caves))

    return cave != 'start' and \
           (cave.isupper() or no_double_small_caves() or cave not in visited)


def find_paths(graph: Dict[str, List[str]],
               start: str,
               end: str,
               next_cave_predicate: Callable[[str, List[str]], bool],
               path: List[str] = None,
               ) -> List[List[str]]:
    """
    All paths from start to end.
    visit small caves at most once only,
        large caves any number of times
    """
    if not path:
        path = [start]

    path_head, *path_tail = path

    # found a path
    if path_head == end:
        return [path]

    next_caves = [
        cave
        for cave
        in graph.get(path_head)
        # if cave.isupper() or cave not in path
        if next_cave_predicate(cave, path)
    ]

    # dead end
    if not next_caves:
        # print(f'dead end: {path}')
        return []

    paths = [
        [next_cave, *path]
        for next_cave
        in next_caves
    ]

    return [
        path
        for route in paths
        for path in find_paths(graph, start, end, next_cave_predicate, route)
    ]


if __name__ == '__main__':
    # graph = parse(test_input[2])
    graph = parse(puzzle_input)
    paths = find_paths(graph, 'start', 'end', next_cave_predicate_puzzle_1)
    for path in paths:
        print(path[::-1])
    print('PUZZLE 1: all paths with small caves at most once: ', len(paths))
    paths = find_paths(graph, 'start', 'end', next_cave_predicate_puzzle_2)
    print('PUZZLE 2: all paths with single small cave at most twice, other small caves at most once: ', len(paths))



import curses
import heapq
from operator import itemgetter
from typing import List, Tuple, Set

from aoc_2021.day_15.input import puzzle_input

test_input = [
    "1163751742",
    "1381373672",
    "2136511328",
    "3694931569",
    "7463417111",
    "1319128137",
    "1359912421",
    "3125421639",
    "1293138521",
    "2311944581",
]


def parse(nodes: List[str]) -> List[List[int]]:
    return [
        [int(n) for n in line]
        for line in nodes
    ]


def shortest_path(graph: List[List[int]],
                  start: Tuple[int, int],
                  end: Tuple[int, int]) -> int:

    def neighbours(node: Tuple[int, int]) -> Set[Tuple[int, int]]:
        width = len(graph[0])
        height = len(graph)
        x0, y0 = node
        return {
            (x0 + x, y0 + y)
            for x in range(-1, 2)
            for y in range(-1, 2)
            if abs(x) != abs(y) and \
            0 <= x0 + x < width and \
            0 <= y0 + y < height
        }

    visited = set()
    to_expand = {start}
    dists = {
        start: 0
    }

    while to_expand:
        # pop node from to_expand closest to start
        # this would be more efficient with heap...
        node, dist = min([(expand, dists.get(expand)) for expand in to_expand], key=itemgetter(1))
        to_expand.remove(node)
        print(f'popped {node} with dist {dist}')
        # update unvisited neighbour distances in dists
        neighbor_nodes = neighbours(node)
        print(f'all neighbours of {node}: {neighbor_nodes}')
        unvisited_neighbors = neighbor_nodes.difference(visited)
        print(f'all visited nodes: {visited}')
        print(f'unvisited neighbours of {node}: {unvisited_neighbors}')
        for x, y in unvisited_neighbors:
            dists[(x, y)] = min((
                dists.get((x, y), float('inf')),
                dists[node] + graph[y][x]
            ))
            print(f'updated neighbour {(x, y)} as {dists[(x, y)]}')
        # add unvisited neighbors into to_expand
        print(f'adding unvisited neighbours {unvisited_neighbors} to to_expand {to_expand}')
        to_expand = to_expand.union(unvisited_neighbors)
        # put current node into visited
        print(f'adding {node} to visited')
        visited.add(node)
        print(dists)
        print('-' * 10)

    return dists.get(end)


if __name__ == '__main__':
    # nodes = parse(test_input)
    nodes = parse(puzzle_input)
    width = len(nodes[0])
    height = len(nodes)
    cost = shortest_path(nodes, start=(0, 0), end=(width - 1, height - 1))
    print(cost)

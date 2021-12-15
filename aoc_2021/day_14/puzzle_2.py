import time
from functools import cache
from itertools import groupby
from typing import Dict, Iterator

from aoc_2021.day_14.input import puzzle_input
from aoc_2021.day_14.puzzle import parse, test_input


def make_replace_dict(rules: Dict[str, str]) -> Dict[str, str]:
    return {
        pair: f"{pair[0]}{middle}{pair[1]}"
        for pair, middle
        in rules.items()
    }


def merge_dicts(d1, d2) -> Dict[str, int]:
    return {
        key: (d1.get(key) or 0) + (d2.get(key) or 0)
        for key
        in set(d1.keys()).union(d2.keys())
    }


def stats(seq: str) -> Dict[str, int]:
    return dict((grouper, len(list(group))) for grouper, group in groupby(sorted(seq)))


def count_freqs(rules: Dict[str, str], pair: str, depth: int) -> Dict[str, int]:
    _counts = dict()

    def _count_freqs(_pair: str, _depth: int):
        a, b = _pair
        if _depth == 0 or _pair not in rules:
            return

        m = rules.get(_pair)

        _counts[m] = _counts.get(m, 0) + 1

        _count_freqs(a + m, _depth - 1)
        _count_freqs(m + b, _depth - 1)
        return

    _count_freqs(pair, depth)
    return _counts


def pairs(seq: str) -> Iterator[str]:
    while len(seq) > 1:
        a, *seq = seq
        yield a + seq[0]


if __name__ == '__main__':
    # start_seq, rules = parse(test_input)
    start_seq, rules = parse(puzzle_input)
    counts = stats(start_seq)
    start = time.time()
    for pair in pairs(start_seq):
        new_counts = count_freqs(rules, pair, 40)
        # print(new_counts)
        counts = merge_dicts(counts, new_counts)
        # print(counts)
    print(time.time() - start, counts)

"""frequencies:  [('B', 1749), ('C', 298), ('H', 161), ('N', 865)]"""

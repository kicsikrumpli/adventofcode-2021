import time
from functools import cache
from itertools import groupby
from typing import Dict, Iterator

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
    # @cache
    def _count_freqs(_pair: str, _depth: int) -> Dict[str, int]:
        if _depth == 0 or _pair not in rules:
            return stats(_pair)

        a, b = _pair
        m = rules.get(_pair)
        return merge_dicts(
            count_freqs(rules, a + m, _depth - 1),
            count_freqs(rules, m + b, _depth - 1)
        )

    return _count_freqs(pair, depth)


def pairs(seq: str) -> Iterator[str]:
    while len(seq) > 1:
        a, *seq = seq
        yield a + seq[0]


if __name__ == '__main__':
    start_seq, rules = parse(test_input)
    print(start_seq)
    for i in range(30):
        counts = dict()
        s = time.time()
        for pair in pairs(start_seq):
            new_counts = count_freqs(rules, pair, i)
            # print(new_counts)
            counts = merge_dicts(counts, new_counts)
            # print(counts)
        print(i, (time.time() - s), counts)

"""{'B': 3497, 'N': 1729, 'C': 596, 'H': 322}"""
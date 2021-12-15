from itertools import groupby
from typing import Iterator, Dict, Tuple

from aoc_2021.day_14.input import puzzle_input
from aoc_2021.day_14.puzzle import parse, test_input


def stats(seq: str) -> Dict[str, int]:
    return dict((grouper, len(list(group))) for grouper, group in groupby(sorted(seq)))


def make_pairs(seq: str) -> Iterator[str]:
    while len(seq) > 1:
        a, *seq = seq
        yield a + seq[0]


def step(rules: Dict[str, str],
         pairs: Dict[str, int],
         counts: Dict[str, int]) -> Tuple[Dict[str, int], Dict[str, int]]:

    new_pairs: Dict[str, int] = dict()
    for pair, no_of_pairs in pairs.items():
        if pair in rules:
            a, b = pair
            m = rules[pair]
            counts[m] = counts.get(m, 0) + no_of_pairs
            new_pairs[a+m] = new_pairs.get(a+m, 0) + no_of_pairs
            new_pairs[m+b] = new_pairs.get(m+b, 0) + no_of_pairs

    return new_pairs, counts


if __name__ == '__main__':
    # start_seq, rules = parse(test_input)
    start_seq, rules = parse(puzzle_input)

    counts = stats(start_seq)
    pairs = {grouper: len(list(group)) for grouper, group in groupby(sorted([pair for pair in make_pairs(start_seq)]))}
    for _ in range(40):
        pairs, counts = step(rules, pairs, counts)
        # print(pairs)
        # print(counts)

    min_freq = min(count for count in counts.values())
    max_freq = max(count for count in counts.values())

    print('max - min after 40 iterations:', max_freq - min_freq)

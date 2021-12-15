from itertools import groupby
from operator import itemgetter
from typing import Tuple, Dict

from aoc_2021.day_14.input import puzzle_input

test_input = """
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
"""


def parse(input_str: str) -> Tuple[str, Dict[str, str]]:
    _, _start_seq, _, *lines, _ = [line.strip() for line in input_str.split('\n')]
    _rules = [
        (seq, ins)
        for seq, ins
        in [rule.split(' -> ') for rule in lines]
    ]
    return _start_seq, dict(_rules)


def insert(rules: Dict[str, str],
           start: str,
           end: str = None,
           ) -> str:

    """
    start  ->   end
    aaaaa[a x b]bbbb
    """
    if end is None:
        *start, end = start

    if not start:
        # consumed all
        return end

    *start_tail, start_head = start
    end_head, *end_tail = end
    middle = rules.get("".join([start_head, end_head]))

    return insert(rules,
                  "".join(start_tail),
                  "".join([*[elem for elem in (start_head, middle, end_head) if elem], *end_tail])
                  )


def nr_insert(rules: Dict[str, str], start: str) -> str:
    """
    same as insert, but non-recursive. easy rewrite for tail-rec fn.
    """
    *start, end = start
    while True:
        if not start:
            return end

        *start_tail, start_head = start
        end_head, *end_tail = end
        middle = rules.get("".join([start_head, end_head]))

        start = "".join(start_tail)
        end = "".join([*[elem for elem in (start_head, middle, end_head) if elem], *end_tail])


if __name__ == '__main__':
    start_seq, rules = parse(test_input)
    # start_seq, rules = parse(puzzle_input)
    seq = start_seq
    # print(seq)
    # for _ in range(4):
    #     seq = insert(rules, seq)
    #     print(seq)

    steps = 10  # puzzle 1
    for step in range(steps):
        print('step ', step)
        seq = nr_insert(rules, seq)

    counts = list((grouper, len(list(group))) for grouper, group in groupby(sorted(seq)))
    sorted_counts = sorted(counts, key=itemgetter(1))
    print('length after 10 steps:', len(seq))
    print('frequencies: ', counts)
    print('min freq:', sorted_counts[0])
    print('max freq:', sorted_counts[-1])
    diff = sorted_counts[-1][1] - sorted_counts[0][1]
    print('most common - least common =', diff)


"""
NNCB
NCNBCHB
NBCCNBBBCBHCB
NBBBCNCCNBBNBNBBCHBHHBCHB
NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB
"""

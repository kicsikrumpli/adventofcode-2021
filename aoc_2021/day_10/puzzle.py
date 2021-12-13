from functools import reduce
from typing import Optional, Tuple

from aoc_2021.day_10.input import puzzle_input

test_inputs = [
    "[({(<(())[]>[[{[]{<()<>>",
    "[(()[<>])]({[<{<<[]>>(",
    "{([(<{}[<>[]}>{[]{[(<()>",
    "(((({<>}<{<{<>}{[]{[]{}",
    "[[<[([]))<([[{}[[()]]]",
    "[{[{({}]{}}([{[{{{}}([]",
    "{<[[]]>}<{[{[{[]{()[[[]",
    "[<(<(<(<{}))><([]([]()",
    "<{([([[(<>()){}]>(<<{{",
    "<{([{{}}[<[[[<>{}]]]>[]]",
]

SYNTAX_ERROR_SCORE = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

AUTOCOMPLETE_SCORE = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}


def consume(line: str, stack: str = "") -> Tuple[Optional[str], Optional[str]]:
    """
    find first syntax error.

    :return: first wrong bracket, None
            or None, autocomplete
    """

    def is_opening(ch: str) -> bool:
        return ch in ('<', '[', '{', '(')

    def is_closing(ch: str) -> bool:
        return ch in ('>', ']', '}', ')')

    def matches(a: str, b: str) -> bool:
        return sorted([a, b]) in (
            ['<', '>'],
            ['[', ']'],
            ['{', '}'],
            ['(', ')'],
        )

    if isinstance(line, list):
        line = "".join(line)

    # print(line, '|', stack)

    if not line:
        # todo! for incomplete check if stack is empty
        return None, stack\
            .replace('[', ']')\
            .replace('(', ')')\
            .replace('<', '>')\
            .replace('{', '}')[::-1]

    head, *tail = line
    if is_opening(head):
        return consume(tail, stack + head)
    elif is_closing(head) and stack:
        *pit, top = stack
        if matches(head, top):
            return consume(tail, "".join(pit))
        else:
            return head, None
    else:
        raise Exception("Unexpected Token")


if __name__ == '__main__':
    # for line_no, test_input in enumerate(test_inputs):
    #     print(f'#{line_no} | {test_input} :', consume(test_input))

    # navigation_subsystem = test_inputs
    navigation_subsystem = puzzle_input
    illegal_sequences = [
        consume(line)
        for line
        in navigation_subsystem
    ]
    # part one
    synstax_errors = [
        synt_err
        for synt_err, _
        in illegal_sequences
        if synt_err
    ]
    score = sum(SYNTAX_ERROR_SCORE.get(ill_char) for ill_char in synstax_errors)
    print('syntax error score:', score)

    # part two
    auto_comps = [
        auto_comp
        for _, auto_comp
        in illegal_sequences
        if auto_comp
    ]
    auto_comp_scores = [
        reduce(lambda x, y: 5 * x + AUTOCOMPLETE_SCORE.get(y), auto_comp, 0)
        for auto_comp
        in auto_comps
    ]
    # print(auto_comp_scores)
    median = list(sorted(auto_comp_scores))[len(auto_comp_scores) // 2]
    print('median autocomplete score:', median)

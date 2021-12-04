from itertools import takewhile
from typing import List, Optional

from aoc_2021.day_04.input import puzzle_input

test_input = """
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
"""


class Bingo:
    def __init__(self, lines: List[str]):
        self.board = [
            int(num.strip())
            for line in lines
            for num in line.split(" ") if num
        ]
        self.done = False

    def draw(self, num: int) -> Optional[int]:
        if not self.done:
            return self._draw(num)
        else:
            return None

    def _draw(self, num: int) -> Optional[int]:
        try:
            num_idx: int = self.board.index(num)
            self.board[num_idx] = None
            if self.is_bingo(num_idx):
                self.done = True
                return self.score(num)
        except ValueError:
            pass
        return None

    def score(self, last_draw: int):
        return last_draw * sum(n for n in self.board if n)

    def is_bingo(self, idx: int):
        row_idx = idx // 5
        col_idx = idx % 5
        row_hit = all(n is None for n in self.board[5 * row_idx: 5 * row_idx+5])
        col_hit = all(n is None for n in self.board[col_idx::5])
        return row_hit or col_hit


def puzzle_parser(puzzle: str):
    lines = [line for line in puzzle.split('\n') if line]
    bingo_numbers = [int(num) for num in lines[0].split(",") if num]
    bingo_boards = [Bingo(lines[i:i+5]) for i in range(1,len(lines), 5)]
    return bingo_numbers, bingo_boards


if __name__ == '__main__':
    # numbers, boards = puzzle_parser(test_input)
    numbers, boards = puzzle_parser(puzzle_input)

    scores = (
        board.draw(num)
        for num in numbers
        for board in boards
    )
    score = [score for score in scores if score]
    print('first:', score[0])
    print('last:', score[-1])

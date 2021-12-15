from operator import itemgetter
from typing import Tuple, List, Optional

from aoc_2021.day_13.input import puzzle_input

test_input = \
    """
    6,10
    0,14
    9,10
    0,3
    10,4
    4,11
    6,0
    6,12
    4,1
    0,13
    10,12
    3,4
    3,0
    8,4
    1,10
    2,14
    8,10
    9,0
    
    fold along y=7
    fold along x=5
    """


def parse(puzzle_str: str) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
    """
    returns [(x, y)], [(0, y) | (x, 0)]
    list of dots, list of fold lines
    """
    _, *lines, _ = [line.strip() for line in puzzle_str.split('\n')]
    split_idx = lines.index('')
    _dots = [
        (int(x), int(y))
        for x, y
        in [line.split(',') for line in lines[:split_idx]]
    ]
    _folds = [
        (None, int(dist)) if axis == 'y' else (int(dist), None)
        for axis, dist
        in [_fold.replace('fold along ', '').split('=') for _fold in lines[split_idx + 1:]]
    ]
    return _dots, _folds


def fold(dots: List[Tuple[int, int]],
         fold_line: Tuple[Optional[int], Optional[int]]) -> List[Tuple[int, int]]:
    def do_fold(dot: [Tuple[int, int]]):
        x, y = dot
        if fold_x is None and y > fold_y:
            y = 2 * fold_y - y
        if fold_y is None and x > fold_x:
            x = 2 * fold_x - x
        return x, y

    fold_x, fold_y = fold_line
    return list(set(do_fold(dot) for dot in dots))


def display(dots: List[Tuple[int, int]],
            fold_line: Tuple[Optional[int], Optional[int]] = (None, None)
            ):
    x_max = max(dots, key=itemgetter(0))[0]
    y_max = max(dots, key=itemgetter(1))[1]
    fold_x, fold_y = fold_line
    for y in range(y_max + 1):
        if fold_x is None and y == fold_y:
            print('-' * (x_max + 1))
        else:
            for x in range(x_max + 1):
                if fold_y is None and x == fold_x:
                    print('|', end='')
                elif (x, y) in dots:
                    print('#', end='')
                else:
                    print(' ', end='')
            print('')


if __name__ == '__main__':
    # dots, folds = parse(test_input)
    dots, folds = parse(puzzle_input)
    for fold_line in folds:
        print('fold line: ', fold_line)
        # display(dots, fold_line)
        dots = fold(dots, fold_line)
        # print('')
        # display(dots)
        # print('')
        print('number of dots after fold:', len(dots))
        # print('')
        # print('')

    display(dots)

"""
###  #### #  # ###  #  # ###  #  # ### 
#  # #    #  # #  # #  # #  # # #  #  #
#  # ###  #  # #  # #  # #  # ##   #  #
###  #    #  # ###  #  # ###  # #  ### 
# #  #    #  # #    #  # #    # #  # # 
#  # ####  ##  #     ##  #    #  # #  #
"""
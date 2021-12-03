import collections
from functools import reduce
from typing import List, Iterable

from aoc_2021.day_03.input import puzzle_input

test_input = [
    0b00100,
    0b11110,
    0b10110,
    0b10111,
    0b10101,
    0b01111,
    0b00111,
    0b11100,
    0b10000,
    0b11001,
    0b00010,
    0b01010,
]


def bits_to_arr(n: int) -> List[int]:
    bits = collections.deque()
    mask = 1
    while n > 0:
        bits.appendleft(n & mask)
        n = n >> 1
    return list(bits)


def add_element_wise(arr_a: List[float], arr_b: List[float]) -> List[float]:
    result = collections.deque()
    while arr_a or arr_b:
        a = arr_a.pop() if arr_a else 0
        b = arr_b.pop() if arr_b else 0
        result.appendleft(a + b)
    return list(result)


def arr_to_bits(arr: List[int]) -> int:
    return reduce(lambda acc, num: acc * 2 + num, arr, 0)


def flip_all(arr: List[int]) -> List[int]:
    return [int(not bit) for bit in arr]


if __name__ == '__main__':
    # input_array = test_input
    input_array = puzzle_input

    nums = [
        [bit / len(input_array) for bit in bits_to_arr(num)]
        for num
        in input_array
    ]
    elementwise_sums = reduce(add_element_wise, nums, [])
    res = [
        int(digit > 0.5)
        for digit
        in elementwise_sums
    ]
    common_ones = arr_to_bits(res)
    common_zeros = arr_to_bits(flip_all(res))
    print(f'{common_ones} * {common_zeros} = {common_ones * common_zeros}')

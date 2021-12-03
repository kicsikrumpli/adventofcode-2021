from functools import reduce
from typing import List, Iterator, Tuple, Callable

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


def bits(n: int) -> Iterator[int]:
    while n > 0:
        yield n & 1
        n = n >> 1


def binary_to_reversed_array(n: int) -> List[int]:
    return [bit for bit in bits(n)]


def pad_right_to_longest(bit_arrays: List[List[int]]) -> List[List[int]]:
    max_len = max(map(len, bit_arrays))
    zeros = [0 for _ in range(max_len)]
    return [
        [*bit_array, *zeros][:max_len]
        for bit_array
        in bit_arrays
    ]


def pop_most_common_left(bit_arrays: List[List[int]]) -> Tuple[int, List[List[int]]]:
    # rmb: right-most bit
    split_lists = [(bits, rmb) for *bits, rmb in bit_arrays]
    most_common_bit = int(sum((rmb for bits, rmb in split_lists)) / len(split_lists) >= 0.5)
    return most_common_bit, [bits
                             for bits, rmb
                             in split_lists
                             if rmb == most_common_bit]


def pop_least_common_left(bit_arrays: List[List[int]]) -> Tuple[int, List[List[int]]]:
    split_lists = [(bits, rmb) for *bits, rmb in bit_arrays]
    least_common_bit = int(sum((rmb for bits, rmb in split_lists)) / len(split_lists) < 0.5)
    return least_common_bit, [bits
                              for bits, rmb
                              in split_lists
                              if rmb == least_common_bit]


def arr_to_bits(arr: List[int]) -> int:
    return reduce(lambda acc, num: acc * 2 + num, arr, 0)


if __name__ == '__main__':
    nums_as_reversed_list = list(map(binary_to_reversed_array, puzzle_input))
    # nums_as_reversed_list = list(map(binary_to_reversed_array, test_input))
    nums_as_padded_reversed_list = pad_right_to_longest(list(nums_as_reversed_list))

    bits_for_most_common = []
    nums = nums_as_padded_reversed_list
    while len(nums) > 1:
        common, nums = pop_most_common_left(nums)
        bits_for_most_common.append(common)
    rest = nums.pop()
    bits_for_most_common = [*bits_for_most_common, *rest[::-1]]
    oxygen_generator_rating = arr_to_bits(bits_for_most_common)
    print('oxygen generator rating', bits_for_most_common, oxygen_generator_rating)

    bits_for_least_common = []
    nums = nums_as_padded_reversed_list
    while len(nums) > 1:
        common, nums = pop_least_common_left(nums)
        bits_for_least_common.append(common)
    rest = nums.pop()
    bits_for_least_common = [*bits_for_least_common, *rest[::-1]]
    co2_scrubber_rating = arr_to_bits(bits_for_least_common)
    print('CO2 scrubber rating', bits_for_least_common, co2_scrubber_rating)
    print(oxygen_generator_rating * co2_scrubber_rating)

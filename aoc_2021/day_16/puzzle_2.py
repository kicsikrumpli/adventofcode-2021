"""
C200B40A82 finds the sum of 1 and 2, resulting in the value 3.
04005AC33890 finds the product of 6 and 9, resulting in the value 54.
880086C3E88112 finds the minimum of 7, 8, and 9, resulting in the value 7.
CE00C43D881120 finds the maximum of 7, 8, and 9, resulting in the value 9.
D8005AC2A8F0 produces 1, because 5 is less than 15.
F600BC2D8F produces 0, because 5 is not greater than 15.
9C005AC2F8F0 produces 0, because 5 is not equal to 15.
9C0141080250320F1802104A08 produces 1, because 1 + 3 = 2 * 2.
"""
import json
import operator
from functools import reduce

from aoc_2021.day_16.input import puzzle_input
from aoc_2021.day_16.puzzle import consume_packets, bitstream

test_inputs = [
    "C200B40A82",
    "04005AC33890",
    "880086C3E88112",
    "CE00C43D881120",
    "D8005AC2A8F0",
    "F600BC2D8F",
    "9C005AC2F8F0",
    "9C0141080250320F1802104A08",
]


def eval(packet: dict) -> dict:
    """
    Packets with type ID 0 are sum packets - their value is the sum of the values of their sub-packets. If they only have a single sub-packet, their value is the value of the sub-packet.
    Packets with type ID 1 are product packets - their value is the result of multiplying together the values of their sub-packets. If they only have a single sub-packet, their value is the value of the sub-packet.
    Packets with type ID 2 are minimum packets - their value is the minimum of the values of their sub-packets.
    Packets with type ID 3 are maximum packets - their value is the maximum of the values of their sub-packets.
    Packets with type ID 5 are greater than packets - their value is 1 if the value of the first sub-packet is greater than the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.
    Packets with type ID 6 are less than packets - their value is 1 if the value of the first sub-packet is less than the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.
    Packets with type ID 7 are equal to packets - their value is 1 if the value of the first sub-packet is equal to the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.
    """
    version = packet['version']
    type_id = packet['type_id']
    val = None
    if type_id == 4:
        val = packet['literal']
    else:
        values = [eval(subpacket)['literal'] for subpacket in packet['subpackets']]
        if type_id == 0:
            val = sum(values)
        elif type_id == 1:
            val = reduce(operator.mul, values, 1)
        elif type_id == 2:
            val = min(values)
        elif type_id == 3:
            val = max(values)
        elif type_id == 5:
            val = int(values[0] > values[1])
        elif type_id == 6:
            val = int(values[0] < values[1])
        elif type_id == 7:
            val = int(values[0] == values[1])

    return {
        'version': version,
        'type_id': 4,
        'literal': val
    }


if __name__ == '__main__':
    # stream = test_inputs[2]
    # for stream in test_inputs:
    #     packet = consume_packets(bitstream(stream))
    #     # print(json.dumps(packet, indent=2))
    #     print('eval of packets:', eval(packet)['literal'])

    packet = consume_packets(bitstream(puzzle_input))
    # print(json.dumps(packet, indent=2))
    print('eval of packets:', eval(packet)['literal'])

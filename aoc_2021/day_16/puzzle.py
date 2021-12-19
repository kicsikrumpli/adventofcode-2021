import json
from typing import Iterator, Generator, Optional, Tuple

from aoc_2021.day_16.input import puzzle_input

test_inputs = [
    "D2FE28",  # literal 2021
    "38006F45291200",  # operator w/ length_type_id = 0, 2 literal subpackets
    "EE00D40C823060",  # operator w/ length_type_id = 1, 3 literal subpackets
    "8A004A801A8002F478",
    "620080001611562C8802118E34",
    "C0015000016115A2E0802F182340",
    "A0016C880162017C3686B18A3D4780",
]


SEGMENT_LEN = 4  # bits in a segment


def bitstream(hex_input: str) -> Iterator[Tuple[str, int, int]]:
    for segment, ch in enumerate(hex_input):
        yield from hex_char_to_bitstream(ch, segment)


def hex_char_to_bitstream(ch: str, segment: int) -> Iterator[Tuple[str, int, int]]:
    n = int(ch, 16)
    for offset, bit in enumerate("{0:04b}".format(n)):
        yield bit, segment, offset


def literal_value_packet(bitstream: Iterator[Tuple[str, int, int]]) -> dict:
    bits = ""
    segment = None
    offset = None
    while True:
        cont_flag, *_ = next(bitstream)
        is_last_group = cont_flag == '0'

        for _ in range(4):
            bit, segment, offset = next(bitstream)
            bits += bit
        if is_last_group:
            break

    return {'literal': int(bits, 2), 'segment': segment, 'offset': offset}


def operator_packet(bitstream: Iterator[Tuple[str, int, int]]) -> dict:
    length_type_id, segment, offset = next(bitstream)
    subpackets = []
    if length_type_id == '0':
        """
        next 15 bits are a number that represents the total length in bits of the sub-packets contained by this packet.
        """
        bits = [next(bitstream) for _ in range(15)]
        total_length_in_bits = int("".join(bit for bit, *_ in bits), 2)
        _, segment, offset = bits[-1]
        start_bit = segment * SEGMENT_LEN + offset + 1
        while segment * SEGMENT_LEN + offset - start_bit + 1 < total_length_in_bits:  # ununsed bits??
            subpacket = consume_packets(bitstream)
            segment = subpacket['segment']
            offset = subpacket['offset']
            subpackets.append(subpacket)

    else:  # length_type_id == '1':
        """
        next 11 bits are a number that represents the number of sub-packets immediately contained by this packet.
        """
        bits = [next(bitstream) for _ in range(11)]
        number_of_sub_packets = int("".join(bit for bit, *_ in bits), 2)
        _, segment, offset = bits[-1]
        for _ in range(number_of_sub_packets):
            subpacket = consume_packets(bitstream)
            segment = subpacket['segment']
            offset = subpacket['offset']
            subpackets.append(subpacket)

    return {'subpackets': subpackets, 'segment': segment, 'offset': offset}


def consume_packets(bitstream: Iterator[Tuple[str, int, int]]) -> 'Packet':
    TYPE_PARSERS = {
        4: literal_value_packet
    }

    version_str = ""
    for _ in range(3):
        version_str_bit, segment, offset = next(bitstream)
        version_str += version_str_bit
    version = int(version_str, 2)

    type_id_str = ""
    for _ in range(3):
        type_id_str_bit, segment, offset = next(bitstream)
        type_id_str += type_id_str_bit
    type_id = int(type_id_str, 2)

    if type_id == 4:
        packet_content = literal_value_packet(bitstream)
    else:
        packet_content = operator_packet(bitstream)

    header = {
        'version': version,
        'type_id': type_id,
        'segment': packet_content['segment'],
        'offset': packet_content['offset']
    }
    return {** header, **packet_content}


def sum_versions(packet: dict) -> int:
    v = packet['version']
    if 'literal' in packet:
        return v
    else:
        return v + sum(sum_versions(subpacket) for subpacket in packet['subpackets'])


if __name__ == '__main__':
    # stream = test_inputs[0]
    # stream = test_inputs[1]
    # stream = test_inputs[2]
    # for idx, (bit, *_) in enumerate(bitstream(stream)):
    #     if idx % 4 == 0:
    #         print(' | ', end='')
    #     print(bit, end='')

    # print('')
    # packet = consume_packets(bitstream(stream))
    # print(json.dumps(packet, indent=2))
    # print('sum of versions:', sum_versions(packet))

    # for stream in test_inputs[3:]:
    #     packet = consume_packets(bitstream(stream))
    #     print('sum of versions:', sum_versions(packet))

    packet = consume_packets(bitstream(puzzle_input))
    print('sum of versions:', sum_versions(packet))


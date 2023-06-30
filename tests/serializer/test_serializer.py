from blast.bitvector import BitVector
from blast.serialize.serializer import BitVectorSerializer

import math


def test_gate_encode():
    assert BitVectorSerializer.encode_gate([0, 0, 0, 0]) == 0
    assert BitVectorSerializer.encode_gate([0, 0, 0, 1]) == 1
    assert BitVectorSerializer.encode_gate([0, 0, 1, 0]) == 2
    assert BitVectorSerializer.encode_gate([0, 1, 0, 0]) == 4
    assert BitVectorSerializer.encode_gate([1, 0, 0, 0]) == 8
    assert BitVectorSerializer.encode_gate([1, 1, 1, 1]) == 15


def test_gate_encode_decode():
    def cycle(gate: list[int]):
        encoded = BitVectorSerializer.encode_gate(gate)
        bit_length = math.ceil(math.log2(len(gate)))
        return BitVectorSerializer.decode_gate(encoded, bit_length)

    assert cycle([0, 0, 0, 0]) == [0, 0, 0, 0]
    assert cycle([0, 0, 0, 1]) == [0, 0, 0, 1]
    assert cycle([0, 0, 1, 0]) == [0, 0, 1, 0]
    assert cycle([0, 1, 0, 0]) == [0, 1, 0, 0]
    assert cycle([1, 0, 0, 0]) == [1, 0, 0, 0]
    assert cycle([1, 1, 1, 1]) == [1, 1, 1, 1]


def test_all(tmp_path_factory):
    bv0 = BitVector.mutable(8)
    bv0[0] = 1
    bv0[1] = 0
    bv0[3] = bv0[2] | bv0[1]
    bv0[4] = bv0[3] & bv0[2]
    bv0[5] = bv0[4] | bv0[3]
    bv0[6] = bv0[5] & bv0[4]
    bv0[7] = bv0[6] | bv0[5]
    serializer0 = BitVectorSerializer(bv0)
    temp_file = tmp_path_factory.mktemp("data").joinpath("sample.yaml")
    serializer0.serialize(temp_file.open("w"))

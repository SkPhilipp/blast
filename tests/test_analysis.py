from blast.bit import Reference, Bit, BitMutable
from blast.bitvector import BitVector
from blast.analysis import BitVectorAnalysis


def test_all():
    vector = BitVector.mutable_from_int(0b1111, 4)
    undetermined_1 = BitMutable()
    undetermined_2 = BitMutable()
    undetermined_3 = BitMutable()
    vector[0:1] = undetermined_1
    vector[2:3] = undetermined_2
    vector[3:4] = undetermined_3
    analysis = BitVectorAnalysis(vector)
    assert analysis.inputs() == {Reference(undetermined_1), Reference(undetermined_2), Reference(undetermined_3)}
    assert analysis.inputs_size() == 2 ** len(analysis.inputs())
    assert analysis.inputs_size_individualized() == 2 * len(analysis.inputs())

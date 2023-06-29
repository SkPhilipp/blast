from blast.bitvector import BitVector
from blast.serialize.serializer import BitVectorSerializer


def test_all():
    bv0 = BitVector.mutable(8)
    bv0[0] = 1
    bv0[3] = bv0[2] | bv0[1]
    bv0[4] = bv0[3] & bv0[2]
    bv0[5] = bv0[4] | bv0[3]
    bv0[6] = bv0[5] & bv0[4]
    bv0[7] = bv0[6] | bv0[5]
    serializer0 = BitVectorSerializer(bv0)
    serializer0.serialize()

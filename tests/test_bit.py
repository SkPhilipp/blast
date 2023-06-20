from blast.bit import Reference, Bit, BitMutable, BIT_0, BIT_1


def test_constants():
    undetermined_1 = BitMutable()
    undetermined_2 = BitMutable()

    # fully concrete
    assert int(~BIT_0) == 1
    assert int(BIT_1 | BIT_0) == 1
    assert int(BIT_1 & BIT_1) == 1
    assert int(BIT_1 ^ BIT_0) == 1

    # representation
    assert repr(BIT_0 | (BIT_1 & undetermined_1)) == "(0 7 (1 1 ?))"

    # inputs
    assert undetermined_1.inputs() == {Reference(undetermined_1)}
    assert (~undetermined_1 | BIT_1).inputs() == {Reference(undetermined_1)}
    assert (undetermined_1 | undetermined_2).inputs() == {Reference(undetermined_1), Reference(undetermined_2)}

    print("OK")

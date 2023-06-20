from blast.bit import Reference, Bit, BitMutable, BIT_0, BIT_1


def test_reference():
    obj_0 = object()
    obj_1 = object()
    obj_2 = object()
    ref_0 = Reference(obj_0)
    ref_1 = Reference(obj_1)
    ref_2 = Reference(obj_2)

    assert ref_0 == ref_0
    assert ref_1 == ref_1
    assert ref_2 == ref_2
    assert ref_0 != ref_1
    assert ref_0 != ref_2
    assert ref_1 != ref_2

    ref_set = {ref_0, ref_1}
    assert ref_0 in ref_set
    assert ref_1 in ref_set
    assert ref_2 not in ref_set

    ref_dict = {ref_0: 0, ref_1: 1}
    assert ref_dict[ref_0] == 0
    assert ref_dict[ref_1] == 1
    assert ref_2 not in ref_dict


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

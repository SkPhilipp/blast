from blast.bitvector import BitVector, bit_len


def test_all():
    # initial properties
    bitvector = BitVector.mutable(bit_len(8))
    assert len(bitvector) == bit_len(8)
    assert not bitvector.is_concrete(bit_len(0), bit_len(8))

    # concrete bit assignment
    bitvector[bit_len(0):bit_len(1)] = 0xff
    bitvector[bit_len(1):bit_len(2)] = 0x01
    bitvector[bit_len(2):bit_len(3)] = 0x10
    assert bitvector.is_concrete(bit_len(0), bit_len(3))
    assert int(bitvector[bit_len(0):bit_len(1)]) == 0xff
    assert int(bitvector[bit_len(1):bit_len(2)]) == 0x01
    assert int(bitvector[bit_len(2):bit_len(3)]) == 0x10
    assert int(bitvector[bit_len(0):bit_len(3)]) == 0xff0110

    # views
    bitvector_view = bitvector[bit_len(0):bit_len(3)]
    assert len(bitvector_view) == bit_len(3)
    assert bitvector_view.is_concrete()
    assert int(bitvector_view[bit_len(0):bit_len(3)]) == 0xff0110

    # operators and simplification
    bitvector_0xf0f0f0 = BitVector.mutable_from_int(0xf0f0f0, bit_len(3))
    bitvector_0x0f0f0f = BitVector.mutable_from_int(0x0f0f0f, bit_len(3))
    assert int((~bitvector_0xf0f0f0)) == 0x0f0f0f
    assert int((~bitvector_0x0f0f0f)) == 0xf0f0f0
    assert int((bitvector_0xf0f0f0 ^ bitvector_0x0f0f0f)) == 0xffffff
    assert int((bitvector_0xf0f0f0 | bitvector_0x0f0f0f)) == 0xffffff
    assert int((bitvector_0xf0f0f0 & bitvector_0x0f0f0f)) == 0x000000

    # rotates
    assert int((bitvector_0xf0f0f0.rotate_right(0))) == 0xf0f0f0
    assert int((bitvector_0xf0f0f0.rotate_right(1))) == 0x787878
    assert int((bitvector_0xf0f0f0.rotate_right(2))) == 0x3c3c3c
    assert int((bitvector_0xf0f0f0.rotate_right(3))) == 0x1e1e1e
    assert int((bitvector_0xf0f0f0.rotate_right(4))) == 0x0f0f0f
    assert int((bitvector_0xf0f0f0.rotate_left(0))) == 0xf0f0f0
    assert int((bitvector_0xf0f0f0.rotate_left(1))) == 0xe1e1e1
    assert int((bitvector_0xf0f0f0.rotate_left(2))) == 0xc3c3c3
    assert int((bitvector_0xf0f0f0.rotate_left(3))) == 0x878787
    assert int((bitvector_0xf0f0f0.rotate_left(4))) == 0x0f0f0f

    # shifts
    bitvector_0xffffff = BitVector.mutable_from_int(0xffffff, bit_len(3))
    assert int((bitvector_0xffffff << 0)) == 0xffffff
    assert int((bitvector_0xffffff << 1)) == 0xfffffe
    assert int((bitvector_0xffffff << 2)) == 0xfffffc
    assert int((bitvector_0xffffff << 3)) == 0xfffff8
    assert int((bitvector_0xffffff << 4)) == 0xfffff0
    assert int((bitvector_0xffffff >> 0)) == 0xffffff
    assert int((bitvector_0xffffff >> 1)) == 0x7fffff
    assert int((bitvector_0xffffff >> 2)) == 0x3fffff
    assert int((bitvector_0xffffff >> 3)) == 0x1fffff
    assert int((bitvector_0xffffff >> 4)) == 0x0fffff

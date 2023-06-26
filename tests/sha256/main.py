from blast.bitvector import BitVector
from blast.sha256.constants import MAGIC_FRACTIONS_BITVECTOR_SQUARE
from blast.sha256.functions import round_big, init_words
from blast.sha256.main import Sha256


def test_all():
    digest_abc = Sha256().finalize(BitVector.mutable_from_int(0x616263, 24))
    assert int(digest_abc[0]) == 0xba7816bf
    assert int(digest_abc[1]) == 0x8f01cfea
    assert int(digest_abc[2]) == 0x414140de
    assert int(digest_abc[3]) == 0x5dae2223
    assert int(digest_abc[4]) == 0xb00361a3
    assert int(digest_abc[5]) == 0x96177a9c
    assert int(digest_abc[6]) == 0xb410ff61
    assert int(digest_abc[7]) == 0xf20015ad

    digest_nothing = Sha256().finalize(BitVector.mutable_from_int(0, 0))
    assert int(digest_nothing[0]) == 0xe3b0c442
    assert int(digest_nothing[1]) == 0x98fc1c14
    assert int(digest_nothing[2]) == 0x9afbf4c8
    assert int(digest_nothing[3]) == 0x996fb924
    assert int(digest_nothing[4]) == 0x27ae41e4
    assert int(digest_nothing[5]) == 0x649b934c
    assert int(digest_nothing[6]) == 0xa495991b
    assert int(digest_nothing[7]) == 0x7852b855

    digest_long = Sha256().finalize(BitVector.mutable_from_int(
        0x6162636462636465636465666465666765666768666768696768696a68696a6b696a6b6c6a6b6c6d6b6c6d6e6c6d6e6f6d6e6f706e6f7071,
        14 * 32))
    assert int(digest_long[0]) == 0x248d6a61
    assert int(digest_long[1]) == 0xd20638b8
    assert int(digest_long[2]) == 0xe5c02693
    assert int(digest_long[3]) == 0x0c3e6039
    assert int(digest_long[4]) == 0xa33ce459
    assert int(digest_long[5]) == 0x64ff2167
    assert int(digest_long[6]) == 0xf6ecedd4
    assert int(digest_long[7]) == 0x19db06c1

    print("OK")

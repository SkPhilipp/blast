from blast.bitvector import BitVector
from blast.sha256.constants import MAGIC_FRACTIONS_BITVECTOR_CUBE, SIZE_WORD


def gamma0(x: BitVector):
    """
    Gamma 0 function as defined in the SHA256 standard.
    :param x:
    :return:
    """
    return x.rotate_right(7) ^ x.rotate_right(18) ^ (x >> 3)


def gamma1(x: BitVector):
    return x.rotate_right(17) ^ x.rotate_right(19) ^ (x >> 10)


def word(position: int):
    """
    :param position:
    :return: A slice representing a 32-bit word from a bitvector representing a word array.
    """
    return slice(position * SIZE_WORD, position * SIZE_WORD + SIZE_WORD)


def init_words(data: BitVector):
    """
    Builds the list of 64 32-bit words used in the SHA256 algorithm.

    :param data: input data from which to retrieve 16 32-bit words
    :return:
    """
    w = BitVector.mutable(SIZE_WORD * 64)
    w[:SIZE_WORD * 16] = data[:16 * SIZE_WORD]
    for wi in range(16, 64):
        w[word(wi)] = gamma1(w[word(wi - 2)]) + w[word(wi - 7)] + gamma0(w[word(wi - 15)]) + w[word(wi - 16)]
    return w


def sigma0(x: BitVector):
    return x.rotate_right(2) ^ x.rotate_right(13) ^ x.rotate_right(22)


def sigma1(x: BitVector):
    return x.rotate_right(6) ^ x.rotate_right(11) ^ x.rotate_right(25)


def choose(x: BitVector, y: BitVector, z: BitVector):
    return z ^ (x & (y ^ z))


def majority(x: BitVector, y: BitVector, z: BitVector):
    return ((x | y) & z) | (x & y)


def round_small(a: BitVector,
                b: BitVector,
                c: BitVector,
                d: BitVector,
                e: BitVector,
                f: BitVector,
                g: BitVector,
                h: BitVector,
                i: int,
                w: BitVector):
    t1 = sigma1(e) + choose(e, f, g) + h + MAGIC_FRACTIONS_BITVECTOR_CUBE[i] + w[word(i)]
    t2 = sigma0(a) + majority(a, b, c)
    return (d + t1), (t2 + t1)


def round_big(h: list[BitVector], w: BitVector, offset: int):
    h[3], h[7] = round_small(h[0], h[1], h[2], h[3], h[4], h[5], h[6], h[7], 0 + offset, w)
    h[2], h[6] = round_small(h[7], h[0], h[1], h[2], h[3], h[4], h[5], h[6], 1 + offset, w)
    h[1], h[5] = round_small(h[6], h[7], h[0], h[1], h[2], h[3], h[4], h[5], 2 + offset, w)
    h[0], h[4] = round_small(h[5], h[6], h[7], h[0], h[1], h[2], h[3], h[4], 3 + offset, w)
    h[3], h[7] = h[7], h[3]
    h[2], h[6] = h[6], h[2]
    h[1], h[5] = h[5], h[1]
    h[0], h[4] = h[4], h[0]

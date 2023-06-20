import sys

from blast.bit import Bit, BitMutable, BIT_1, BIT_0


def bit_len(byte_len):
    return byte_len * 8


# noinspection PyProtectedMember
class BitVector(object):
    """
    A symbolic bitvector is a vector of symbolic bits; a utility for symbolic bit bulk operations.
    """

    def __init__(self, bits):
        """
        :param Bit[] bits: list of symbolic bits to represent the vector
        """
        self._bits = bits
        self._last_call_id_complexity = None
        self._last_call_id_simplify = None
        self._last_complexity = None

    @staticmethod
    def dynamic(length):
        """
        Creates a symbolic bit vector containing dynamic symbolic bits.

        :param int length: Length of bit-vector, in bits
        :rtype: BitVector
        """
        bits = [BitMutable() for _ in range(length)]
        return BitVector(bits)

    @staticmethod
    def from_int(value, length):
        bv = BitVector.dynamic(length)
        bv[0:length] = value
        return bv

    def _valid_slice(self, item):
        """
        Returns a slice with start and stop indices within this bit vector's range.
        :param item:
        :return:
        """
        if type(item) is int:
            return slice(item, item + 1)
        if type(item) is slice:
            start = item.start if item.start is not None else 0
            stop = item.stop if item.stop is not None else len(self)
            return slice(start, stop)
        raise TypeError("Invalid type for item: {}".format(type(item)))

    def __getitem__(self, item):
        """
        Returns an independently modifiable view on the symbolic bit vector for the given item.

        :param item: An integer or a slice, interpreted as bit indices
        :rtype: BitVector
        """
        valid_slice = self._valid_slice(item)
        return BitVector(self._bits[valid_slice])

    def _write_symbolic(self, bit_start_inclusive, bits, value):
        """
        Writes symbolic bits into this symbolic bit vector.

        :param int bit_start_inclusive: Start index of bit-vector, in bits
        :param int bits: Amount of bits of value to write
        :param BitVector value: Value to assign to bit-vector
        """
        for i in range(bit_start_inclusive, bit_start_inclusive + bits):
            self._bits[i] = value._bits[i - bit_start_inclusive]

    def _write_concrete(self, bit_start_inclusive, bits, value):
        """
        Writes concrete bits as symbolic bits into this symbolic bit vector.

        :param int bit_start_inclusive: Start index of bit-vector, in bits
        :param int bits: Amount of bits of value to write
        :param int value: Value to assign to bit-vector
        """
        for i in reversed(range(bit_start_inclusive, bit_start_inclusive + bits)):
            symbolic_bit = BIT_1 if value & 1 else BIT_0
            self._bits[i] = symbolic_bit
            value >>= 1

    def __setitem__(self, item, value):
        """
        Sets the symbolic bits at the given key to the given value.

        :param item: Either an integer or a slice, interpreted as bit indices
        :param value: Either a symbolic bit vector, or an integer
        """
        valid_slice = self._valid_slice(item)
        bits = valid_slice.stop - valid_slice.start if type(valid_slice) is slice else 1
        if type(value) == BitVector:
            self._write_symbolic(valid_slice.start, bits, value)
        if type(value) == int:
            self._write_concrete(valid_slice.start, bits, value)

    def is_concrete(self, bit_start_inclusive=0, bits=sys.maxsize):
        """
        Checks if all symbolic bits in the given range are concrete.

        :param int bit_start_inclusive: Start index of bit-vector, in bits
        :param int bits: Amount of bits to check
        :return: True if all bits are concrete
        :rtype: bool
        """
        for bit in self._bits[bit_start_inclusive:bit_start_inclusive + bits]:
            if not bit.is_concrete():
                return False
        return True

    def __int__(self):
        """
        Converts the symbolic bit vector to an integer by inferring each bit's concrete value.

        :return:
        """
        value = 0
        for i in range(len(self._bits)):
            value <<= 1
            value |= int(self._bits[i])
        return value

    def __str__(self):
        """
        Converts the bit vector to a string of hexadecimal digits.
        :return:
        """
        return hex(int(self))

    def __repr__(self):
        return "[" + ", ".join(str(bit) for bit in self._bits) + "]"

    def __len__(self):
        return len(self._bits)

    def rotate_right(self, bits):
        """
        Bitwise rotate the bit vector right by the given amount of bits, returning a new bit vector.
        :param bits:
        :return:
        """
        bv = self[:]
        for i in range(len(bv._bits)):
            bv._bits[i] = self._bits[(i - bits) % len(bv._bits)]
        return bv

    def rotate_left(self, bits):
        """
        Bitwise rotate the bit vector left by the given amount of bits, returning a new bit vector.
        :param bits:
        :return:
        """
        return self.rotate_right(len(self) - bits)

    def __invert__(self):
        """
        Bitwise invert the bit vector, returning a new bit vector.
        :return:
        """
        bv = self[:]
        for i in range(len(bv._bits)):
            bv._bits[i] = ~bv._bits[i]
        return bv

    def __xor__(self, other):
        """
        Bitwise exclusive or the bit vector with another bit vector, returning a new bit vector.
        :param other:
        :return:
        """
        if len(self._bits) != len(other._bits):
            raise ValueError("Bit vectors must have the same length")
        bv = self[:]
        for i in range(len(bv._bits)):
            bv._bits[i] = bv._bits[i] ^ other._bits[i]
        return bv

    def __and__(self, other):
        """
        Bitwise and the bit vector with another bit vector, returning a new bit vector.
        :param other:
        :return:
        """
        if len(self._bits) != len(other._bits):
            raise ValueError("Bit vectors must have the same length")
        bv = self[:]
        for i in range(len(bv._bits)):
            bv._bits[i] = bv._bits[i] & other._bits[i]
        return bv

    def __or__(self, other):
        """
        Bitwise or the bit vector with another bit vector, returning a new bit vector.
        :param other:
        :return:
        """
        if len(self._bits) != len(other._bits):
            raise ValueError("Bit vectors must have the same length")
        bv = self[:]
        for i in range(len(bv._bits)):
            bv._bits[i] = bv._bits[i] | other._bits[i]
        return bv

    def __rshift__(self, bits):
        """
        Bitwise right shift the bit vector by the given amount of bits, returning a new bit vector.
        :param bits:
        :return:
        """
        if type(bits) != int:
            raise ValueError("Right shift amount must be an integer")
        if bits < 0:
            raise ValueError("Right shift amount must be non-negative")
        bv = self.rotate_right(bits)
        for i in range(bits):
            bv._bits[i] = BIT_0
        return bv

    def __lshift__(self, bits):
        """
        Bitwise left shift the bit vector by the given amount of bits, returning a new bit vector.
        :param bits:
        :return:
        """
        if type(bits) != int:
            raise ValueError("Left shift amount must be an integer")
        if bits < 0:
            raise ValueError("Left shift amount must be non-negative")
        bv = self.rotate_left(bits)
        for i in range(len(bv._bits) - bits, len(bv._bits)):
            bv._bits[i] = BIT_0
        return bv

    def __add__(self, other):
        """
        Bitwise sum of the bit vector with another bit vector, returning a new bit vector.
        Any bits that overflow the length of the bit vector are discarded.
        :param other:
        :return:
        """
        if len(self._bits) != len(other._bits):
            raise ValueError("Bit vectors must have the same length")
        if self.is_concrete() and other.is_concrete():
            return BitVector.from_int(int(self) + int(other), len(self))
        bv = self[:]
        carry = BIT_0
        for i in range(len(bv._bits)):
            bv._bits[i], carry = Bit.add(bv._bits[i], other._bits[i], carry)
        return bv

    def __sub__(self, other):
        """
        Bitwise subtraction of the bit vector with another bit vector, returning a new bit vector.
        Supports underflow.
        :param other:
        :return:
        """
        if not self.is_concrete():
            raise ValueError("Bit vector is not concrete")
        if not other.is_concrete():
            raise ValueError("Bit vector is not concrete")
        result = int(self) + int(other)
        if result < 0:
            result += 2 ** len(self)
        return BitVector.from_int(result, len(self))


if __name__ == "__main__":
    # initial properties
    bitvector = BitVector.dynamic(bit_len(8))
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
    bitvector_0xf0f0f0 = BitVector.from_int(0xf0f0f0, bit_len(3))
    bitvector_0x0f0f0f = BitVector.from_int(0x0f0f0f, bit_len(3))
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
    bitvector_0xffffff = BitVector.from_int(0xffffff, bit_len(3))
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

    print("OK")

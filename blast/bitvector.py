import sys

from typing import Self
from blast.bit import Bit, BitMutable, BIT_1, BIT_0


def bit_len(byte_len):
    return byte_len * 8


class BitVector(object):
    """
    BitsOperator represents a vector of bits, where each element is either a concrete (BitMutable) or symbolic (BitOperator).
    """

    def __init__(self, bits: [Bit]):
        """
        :param bits: Underlying Bit objects together representing a bit-vector.
        """
        self._bits = bits

    @staticmethod
    def mutable(length: int):
        """
        Create a new mutable bit-vector of the given length.

        :param length: Length of bit-vector, in bits
        """
        bits = [BitMutable() for _ in range(length)]
        return BitVector(bits)

    @staticmethod
    def mutable_from_int(value: int, length: int):
        """
        Create a new mutable bit-vector of the given length, initialized with the given value.
        :param value:
        :param length:
        :return:
        """
        bv = BitVector.mutable(length)
        bv[0:length] = value
        return bv

    def _valid_slice(self, item: slice | int) -> slice:
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

    def __getitem__(self, item: slice | int) -> Self:
        """
        Returns an independently modifiable view of this bit vector for the given item.

        :param item: An integer or a slice, interpreted as bit indices
        """
        valid_slice = self._valid_slice(item)
        return BitVector(self._bits[valid_slice])

    def _write_bitvector(self, start_inclusive: int, length: int, source: Self):
        """
        Copy elements of another bit-vector into this bit-vector.

        :param start_inclusive: Start index within this bit-vector, in bits
        :param length: Amount of elements to copy
        :param source: Bit-vector to copy from
        """
        for i in range(start_inclusive, start_inclusive + length):
            self._bits[i] = source._bits[i - start_inclusive]

    def _write_int(self, start_inclusive: int, length: int, source: int):
        """
        Copy concrete bits of an integer into this bit-vector.

        :param start_inclusive: Start index within this bit-vector, in bits
        :param length: Amount of bits to copy
        :param source: Integer to copy from
        """
        for i in reversed(range(start_inclusive, start_inclusive + length)):
            symbolic_bit = BIT_1 if source & 1 else BIT_0
            self._bits[i] = symbolic_bit
            source >>= 1

    def __setitem__(self, item: slice | int, value: Self | int):
        """
        Assigns the given bit-vector or integer to the given bit indices.

        :param item: An integer or a slice, interpreted as bit indices
        :param value: A bit-vector or an integer to copy from
        """
        valid_slice = self._valid_slice(item)
        bits = valid_slice.stop - valid_slice.start if type(valid_slice) is slice else 1
        if type(value) == BitVector:
            self._write_bitvector(valid_slice.start, bits, value)
        elif type(value) == int:
            self._write_int(valid_slice.start, bits, value)
        else:
            raise TypeError("Invalid type for value: {}".format(type(value)))

    def is_concrete(self, bit_start_inclusive: int = 0, bits: int = sys.maxsize) -> bool:
        """
        Checks if all symbolic bits in the given range are concrete.

        :param bit_start_inclusive: Start index within this bit-vector, in bits
        :param bits: Amount of bits to check
        :return: True if all bits are concrete, False otherwise
        """
        for bit in self._bits[bit_start_inclusive:bit_start_inclusive + bits]:
            if not bit.is_concrete():
                return False
        return True

    def __int__(self) -> int:
        """
        Converts the symbolic bit vector to an integer by inferring each element's concrete value.
        :return:
        """
        value = 0
        for i in range(len(self._bits)):
            value <<= 1
            value |= int(self._bits[i])
        return value

    def __str__(self) -> str:
        """
        Converts the bit vector to a string of hexadecimal digits.
        :return:
        """
        return hex(int(self))

    def __repr__(self) -> str:
        return "[" + ", ".join(str(bit) for bit in self._bits) + "]"

    def __len__(self) -> int:
        return len(self._bits)

    def rotate_right(self, amount: int) -> Self:
        """
        Create a new bit vector with its bits bitwise rotated right by the given amount of bits.
        :param amount:
        :return:
        """
        bv = self[:]
        for i in range(len(bv._bits)):
            bv._bits[i] = self._bits[(i - amount) % len(bv._bits)]
        return bv

    def rotate_left(self, amount: int) -> Self:
        """
        Create a new bit vector with its bits bitwise rotated left by the given amount of bits.
        :param amount:
        :return:
        """
        return self.rotate_right(len(self) - amount)

    def __invert__(self) -> Self:
        """
        Create a new bit vector with its bits inverted.
        :return:
        """
        bv = self[:]
        for i in range(len(bv._bits)):
            bv._bits[i] = ~bv._bits[i]
        return bv

    def __xor__(self, other: Self) -> Self:
        """
        Create a new bit vector with its bits bitwise XOR'ed with another bit vector.
        :param other:
        :return:
        """
        if len(self._bits) != len(other._bits):
            raise ValueError("Bit vectors must have the same length")
        bv = self[:]
        for i in range(len(bv._bits)):
            bv._bits[i] = bv._bits[i] ^ other._bits[i]
        return bv

    def __and__(self, other: Self) -> Self:
        """
        Create a new bit vector with its bits bitwise AND'ed with another bit vector.
        :param other:
        :return:
        """
        if len(self._bits) != len(other._bits):
            raise ValueError("Bit vectors must have the same length")
        bv = self[:]
        for i in range(len(bv._bits)):
            bv._bits[i] = bv._bits[i] & other._bits[i]
        return bv

    def __or__(self, other: Self) -> Self:
        """
        Create a new bit vector with its bits bitwise OR'ed with another bit vector.
        :param other:
        :return:
        """
        if len(self._bits) != len(other._bits):
            raise ValueError("Bit vectors must have the same length")
        bv = self[:]
        for i in range(len(bv._bits)):
            bv._bits[i] = bv._bits[i] | other._bits[i]
        return bv

    def __rshift__(self, amount) -> Self:
        """
        Create a new bit vector with its bits bitwise right shifted by the given amount of bits.
        :param amount:
        :return:
        """
        if type(amount) != int:
            raise ValueError("Right shift amount must be an integer")
        if amount < 0:
            raise ValueError("Right shift amount must be non-negative")
        bv = self.rotate_right(amount)
        for i in range(amount):
            bv._bits[i] = BIT_0
        return bv

    def __lshift__(self, amount) -> Self:
        """
        Create a new bit vector with its bits bitwise left shifted by the given amount of bits.
        :param amount:
        :return:
        """
        if type(amount) != int:
            raise ValueError("Left shift amount must be an integer")
        if amount < 0:
            raise ValueError("Left shift amount must be non-negative")
        bv = self.rotate_left(amount)
        for i in range(len(bv._bits) - amount, len(bv._bits)):
            bv._bits[i] = BIT_0
        return bv

    def __add__(self, other: Self) -> Self:
        """
        Create a new bit vector with its bits bitwise added with another bit vector.
        The bit overflowing the length of the bit vector is discarded.
        :param other:
        :return:
        """
        if len(self._bits) != len(other._bits):
            raise ValueError("Bit vectors must have the same length")
        if self.is_concrete() and other.is_concrete():
            return BitVector.mutable_from_int(int(self) + int(other), len(self))
        bv = self[:]
        carry = BIT_0
        for i in range(len(bv._bits)):
            bv._bits[i], carry = Bit.add(bv._bits[i], other._bits[i], carry)
        return bv

    def __sub__(self, other: Self) -> Self:
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
        return BitVector.mutable_from_int(result, len(self))


if __name__ == "__main__":
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

    print("OK")

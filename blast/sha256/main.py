import math

from blast.bitvector import BitVector
from blast.sha256.constants import MAGIC_FRACTIONS_BITVECTOR_SQUARE
from blast.sha256.functions import round_big, init_words


class Sha256(object):
    """
    SHA256 implementation, implemented as described in the FIPS PUB 180-4 standard.

    Operates on symbolic bitvectors.
    """

    def __init__(self):
        self.digest = MAGIC_FRACTIONS_BITVECTOR_SQUARE[:]

    def _transform(self, data):
        w = init_words(data)

        ss = self.digest[:]

        round_big(ss, w, 0)
        round_big(ss, w, 4)
        round_big(ss, w, 8)
        round_big(ss, w, 12)
        round_big(ss, w, 16)
        round_big(ss, w, 20)
        round_big(ss, w, 24)
        round_big(ss, w, 28)
        round_big(ss, w, 32)
        round_big(ss, w, 36)
        round_big(ss, w, 40)
        round_big(ss, w, 44)
        round_big(ss, w, 48)
        round_big(ss, w, 52)
        round_big(ss, w, 56)
        round_big(ss, w, 60)

        self.digest[0] = self.digest[0] + ss[0]
        self.digest[1] = self.digest[1] + ss[1]
        self.digest[2] = self.digest[2] + ss[2]
        self.digest[3] = self.digest[3] + ss[3]
        self.digest[4] = self.digest[4] + ss[4]
        self.digest[5] = self.digest[5] + ss[5]
        self.digest[6] = self.digest[6] + ss[6]
        self.digest[7] = self.digest[7] + ss[7]

    @staticmethod
    def pad(message):
        """
        Pads the given message to create 512 bits of data, according to the SHA-256 standard.

        The message is padded with a 1 bit, followed by 0 bits, followed by 64 bits indicating message length
        making the total length of the message 512 bits.
        :return:
        """
        len_message = len(message)
        len_padded = math.ceil((len_message + 1 + 64) / 512) * 512
        data = BitVector.mutable(len_padded)
        data[:len_message] = message
        data[len_message] = 1
        data[len_message + 1: len(data) - 64] = 0
        data[len(data) - 64:] = BitVector.mutable_from_int(len_message, 64)
        return data

    def finalize(self, known_input: BitVector):
        """
        :param known_input: Any known characteristics of the input encoded as a symbolic bitvector with at least a known length.
        :rtype: BitVector[]
        """
        data = self.pad(known_input)
        for i in range(0, len(data), 512):
            self._transform(data[i:i + 512])
        return self.digest

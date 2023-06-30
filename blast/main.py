import sys
import typing

from blast.sha256.constants import SIZE_WORD
from blast.sha256.functions import gamma0, gamma1, sigma0, sigma1
from blast.bitvector import BitVector
from blast.serialize.serializer import BitVectorSerializer, BitVectorDeserializer


class Dump(object):
    def __init__(self, source: BitVector, stream: typing.IO):
        self._source = source
        self._stream = stream

    def gamma0(self):
        source = self._source if self._source is not None else BitVector.mutable(SIZE_WORD)
        bitvector = gamma0(source)
        BitVectorSerializer.serialize(bitvector, self._stream)

    def gamma1(self):
        source = self._source if self._source is not None else BitVector.mutable(SIZE_WORD)
        bitvector = gamma1(source)
        BitVectorSerializer.serialize(bitvector, self._stream)

    def sigma0(self):
        source = self._source if self._source is not None else BitVector.mutable(SIZE_WORD)
        bitvector = sigma0(source)
        BitVectorSerializer.serialize(bitvector, self._stream)

    def sigma1(self):
        source = self._source if self._source is not None else BitVector.mutable(SIZE_WORD)
        bitvector = sigma1(source)
        BitVectorSerializer.serialize(bitvector, self._stream)


class CLI(object):

    def __init__(self, infile: str = "-", outfile: str = "-"):
        input_stream = sys.stdin if infile == "-" else open(infile, "r")
        output_stream = sys.stdout if outfile == "-" else open(outfile, "w")
        source = None if input_stream.isatty() else BitVectorDeserializer.deserialize(input_stream)
        self.dump = Dump(source, output_stream)

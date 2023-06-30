import sys
import typing

from blast.analysis import BitVectorAnalysis
from blast.sha256.constants import SIZE_WORD
from blast.sha256.functions import gamma0, gamma1, sigma0, sigma1
from blast.bitvector import BitVector
from blast.serialize.serializer import BitVectorSerializer, BitVectorDeserializer


class SubcommandDump(object):
    def __init__(self, source: BitVector, stream: typing.IO):
        self._source = source
        self._stream = stream

    def gamma0(self):
        """
        Serialize the gamma0 function.
        """
        source = self._source if self._source is not None else BitVector.mutable(SIZE_WORD)
        bitvector = gamma0(source)
        BitVectorSerializer.serialize(bitvector, self._stream)

    def gamma1(self):
        """
        Serialize the gamma1 function.
        """
        source = self._source if self._source is not None else BitVector.mutable(SIZE_WORD)
        bitvector = gamma1(source)
        BitVectorSerializer.serialize(bitvector, self._stream)

    def sigma0(self):
        """
        Serialize the sigma0 function.
        """
        source = self._source if self._source is not None else BitVector.mutable(SIZE_WORD)
        bitvector = sigma0(source)
        BitVectorSerializer.serialize(bitvector, self._stream)

    def sigma1(self):
        """
        Serialize the sigma1 function.
        """
        source = self._source if self._source is not None else BitVector.mutable(SIZE_WORD)
        bitvector = sigma1(source)
        BitVectorSerializer.serialize(bitvector, self._stream)

    def bit(self, index: int):
        """
        Serialize a bit at the given index.
        """
        if self._source is None:
            raise ValueError("A source must be provided")
        bit = self._source[index:index + 1]
        BitVectorSerializer.serialize(bit, self._stream)


class SubcommandAnalysis(object):
    def __init__(self, source: BitVector, stream: typing.IO):
        self._source = source
        self._stream = stream

    def individualized(self):
        if self._source is None:
            raise ValueError("A source must be provided")
        analysis = BitVectorAnalysis(self._source)
        analysis_individualized = analysis.individualize()
        print(f"Individualized:")
        for analysis_bit in analysis_individualized:
            print(f"- {analysis_bit.compute()}")


class CLI(object):

    def __init__(self, infile: str = "-", outfile: str = "-"):
        input_stream = sys.stdin if infile == "-" else open(infile, "r")
        output_stream = sys.stdout if outfile == "-" else open(outfile, "w")
        source = None if input_stream.isatty() else BitVectorDeserializer.deserialize(input_stream)
        self.dump = SubcommandDump(source, output_stream)
        self.analysis = SubcommandAnalysis(source, output_stream)

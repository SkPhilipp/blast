import sys

from blast.sha256.constants import SIZE_WORD
from blast.sha256.functions import gamma0
from blast.bitvector import BitVector
from blast.serialize.serializer import BitVectorSerializer


class CLI(object):

    def __init__(self, file: str = "-"):
        self.file = file

    def _setup(self):
        if self.file == "-":
            self.file = sys.stdout
        else:
            self.file = open(self.file, "w")

    def dump_gamma0(self):
        self._setup()
        bitvector = gamma0(BitVector.mutable(SIZE_WORD))
        BitVectorSerializer.serialize(bitvector, self.file)

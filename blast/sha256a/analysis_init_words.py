from blast.sha256.constants import SIZE_WORD
from blast.sha256.functions import gamma0
from blast.bitvector import BitVector
from blast.analysis import BitVectorAnalysis


def run():
    analysis_gamma0 = BitVectorAnalysis(gamma0(BitVector.mutable(SIZE_WORD)))
    analysis_gamma0_individualized = analysis_gamma0.individualize()
    print(analysis_gamma0)
    for i in range(len(analysis_gamma0_individualized)):
        item = analysis_gamma0_individualized[i]
        print(f"{i}: {item.compute()}")


if __name__ == "__main__":
    run()

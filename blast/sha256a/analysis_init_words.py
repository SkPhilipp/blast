from blast.sha256.constants import SIZE_WORD
from blast.sha256.functions import gamma0, gamma1, word, init_words
from blast.bitvector import BitVector
from blast.analysis import BitVectorAnalysis


def run():
    analysis_gamma0 = BitVectorAnalysis(gamma0(BitVector.mutable(SIZE_WORD)))
    print(analysis_gamma0.inputs_size())
    print(analysis_gamma0.inputs_size_individualized())

    analysis_gamma1 = BitVectorAnalysis(gamma1(BitVector.mutable(SIZE_WORD)))
    print(analysis_gamma1.inputs_size())
    print(analysis_gamma1.inputs_size_individualized())

    init_words_vector = init_words(BitVector.mutable(SIZE_WORD * 16))
    analysis_init_words = BitVectorAnalysis(init_words_vector[word(16)])
    print(analysis_init_words.inputs_size())
    print(analysis_init_words.inputs_size_individualized())


if __name__ == "__main__":
    run()

from blast.sha256.constants import SIZE_WORD
from blast.sha256.functions import gamma0, gamma1, word, init_words
from blast.sha256.main import Sha256
from blast.bitvector import BitVector
from blast.analysis import BitVectorAnalysis


def run():
    analysis_gamma0 = BitVectorAnalysis(gamma0(BitVector.mutable(SIZE_WORD)))
    print(analysis_gamma0.inputs_len())
    print(analysis_gamma0.inputs_len_individualized())

    analysis_gamma1 = BitVectorAnalysis(gamma1(BitVector.mutable(SIZE_WORD)))
    print(analysis_gamma1.inputs_len())
    print(analysis_gamma1.inputs_len_individualized())

    padded = Sha256.pad(BitVector.mutable(256))
    analysis_padded = BitVectorAnalysis(padded)
    print(analysis_padded.inputs_len())
    print(analysis_padded.inputs_len_individualized())

    init_words_vector = init_words(padded)
    analysis_init_words = BitVectorAnalysis(init_words_vector[word(17)])
    print(analysis_init_words.inputs_len())
    print(analysis_init_words.inputs_len_individualized())


if __name__ == "__main__":
    run()

from blast.bit import Reference, Bit, BitMutable
from blast.bitvector import BitVector


class BitVectorAnalysis(object):
    def __init__(self, bit_vector: BitVector):
        self.bit_vector: BitVector = bit_vector

    def inputs(self) -> set[Reference]:
        """
        Return the distinct input bits of the underlying bit vector.
        :return:
        """
        inputs = set()
        for i in range(len(self.bit_vector)):
            bit = self.bit_vector.bit(i)
            for reference in bit.inputs():
                if isinstance(reference.value, BitMutable):
                    inputs.add(reference)
        return inputs

    def inputs_size(self) -> int:
        """
        Return the size of the set of all possible input values.
        For example; if the bitvector has 4 input bits, this will return 16 (2^4).
        :return:
        """
        inputs_len = len(self.inputs())
        if inputs_len == 0:
            return 0
        return 2 ** inputs_len

    def inputs_size_individualized(self) -> int:
        """
        Return the sum of size of the set of all possible input values for each element in the bitvector.
        For example; if the bitvector has 4 elements operating on 1 input bit each, this will return 8 (2^1 + 2^1 + 2^1 + 2^1).
        :return:
        """
        inputs_size = 0
        for i in range(len(self.bit_vector)):
            bit = self.bit_vector.bit(i)
            inputs_len = len(bit.inputs())
            if inputs_len > 0:
                inputs_size += 2 ** len(bit.inputs())
        return inputs_size

    def outputs(self) -> set[Reference]:
        """
        Return the distinct elements of the underlying bit vector.
        :return:
        """
        pass

    def outputs_size(self) -> int:
        """
        Return the size of the set of all possible output values.
        :return:
        """
        return 2 ** len(self.outputs())

    def constraints(self) -> set[Reference]:
        """
        Return the constraints applied to computations.
        :return:
        """
        pass

    def constraint_add(self, expression: Bit):
        """
        Constrains future computations to only be performed when the given expression is true.
        :param expression:
        :return:
        """
        pass

    def constraint_remove(self, expression: Bit):
        """
        Removes a constraint.
        :param expression:
        :return:
        """
        pass

    def compute(self, input_range: range) -> bytearray:
        """
        Compute the output of the bitvector for the given input range.
        :param input_range:
        :return:
        """
        pass

    def compute_individualized(self, input_range: range) -> bytearray:
        """
        Compute the output of the bitvector for the given input range, for each element in the bitvector separately.
        :param input_range:
        :return:
        """
        pass

    def compute_hash(self, input_range: range) -> bytearray:
        """
        Compute the fingerprint of the bitvector for the given input range.
        :param input_range:
        :return:
        """
        pass

    def compute_loop_iterations(self, limit: int) -> int | None:
        """
        Computes how many iterations are required to get back the original input.
        Can only be performed on a bitvector where the size of outputs equals size of inputs.
        :param limit: Maximum number of iterations to try.
        :return:
        """
        pass

    def loop_build(self, iterations: int) -> BitVector:
        """
        Builds a BitVector which re-invokes itself for the given number of iterations.
        Can only be performed on a bitvector where the size of outputs equals size of inputs.
        :param iterations:
        :return:
        """
        pass

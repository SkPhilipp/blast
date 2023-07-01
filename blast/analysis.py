from blast.bit import Reference, Bit, BitMutable
from blast.bitvector import BitVector


class BitVectorAnalysis(object):
    def __init__(self, bit_vector: BitVector):
        self.bit_vector: BitVector = bit_vector

    def individualize(self) -> ['BitVectorAnalysis']:
        """
        Create a BitVectorAnalysis for each bit in the underlying bitvector.
        :return:
        """
        analyses = []
        for i in range(len(self.bit_vector)):
            analyses.append(BitVectorAnalysis(self.bit_vector[i:i + 1]))
        return analyses

    def inputs(self) -> list[Reference]:
        """
        Return the distinct non-concrete input bits required to resolve the bitvector, sorted by reference.
        :return:
        """
        inputs = set()
        for i in range(len(self.bit_vector)):
            bit = self.bit_vector.bit(i)
            for reference in bit.inputs():
                if not isinstance(reference.value, BitMutable):
                    continue
                if reference.value.is_concrete():
                    continue
                inputs.add(reference)
        return sorted(inputs)

    def outputs(self) -> set[Reference]:
        """
        Return the distinct elements of the underlying bit vector.
        :return:
        """
        outputs = set()
        for i in range(len(self.bit_vector)):
            outputs.add(Reference(self.bit_vector.bit(i)))
        return outputs

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

    def compute(self, input_range: range | None = None) -> [int]:
        """
        Compute the output of the bitvector for the given input range.
        :param input_range:
        :return:
        """
        results = []
        inputs = list(self.inputs())
        inputs.sort()
        if input_range is None:
            input_range = range(2 ** len(inputs))
        for i_computation in input_range:
            for i_input in range(len(inputs)):
                value = (i_computation >> i_input) & 1
                inputs[i_input].value.assign(value)
            result = int(self.bit_vector)
            results.append(result)
        for element in inputs:
            element.value.assign(None)
        return results

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

    def __str__(self):
        return f"BitVectorAnalysis({self.bit_vector})"

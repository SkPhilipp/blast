from blast.bit import Bit, BitExpression, BIT_0
from blast.analysis import BitVectorAnalysis


class BitExpressionOptimization(object):
    @staticmethod
    def _fix_inputs(inputs: [Bit], gate: [int]) -> Bit | None:
        """
        Returns an optimized expression, or None if no optimization is possible.
        This method determines for a given gate whether the given inputs' values have any effect on the gate's outputs.

        For example;
        - For a gate of [0, 0, 0, 0] the inputs have no effect on the outputs; it always maps to 0.
        - For a gate of [0, 1, 0, 1] the highest bit input has no effect on the outputs; it always maps to [0, 1].

        The optimized expression is formed by replacing the inputs which have no effect on the outputs with a constant bit.

        :param inputs: The inputs bits to the expression which formed the outputs.
        :param gate: The computed outputs for each possible input permutation.
        :return: An optimized expression, or None.
        """
        if 2 ** len(inputs) != len(gate):
            raise ValueError(f"Can't apply this optimization to {len(inputs)} inputs for a gate size of {len(gate)}.")

        inputs_new = list(inputs)
        inputs_modified = False
        sections = 1
        for input_index in reversed(range(len(inputs))):
            # check if all sections' left halves equal their right halves
            section_length = len(gate) // sections
            section_length_half = section_length // 2
            section_halves_match = True
            for i in range(sections):
                section_offset = i * section_length
                section_offset_half_right = section_offset + section_length_half
                for j in range(section_length_half):
                    if gate[section_offset + j] != gate[section_offset_half_right + j]:
                        section_halves_match = False
                        break
                if not section_halves_match:
                    break
            # when halves match, the input has no effect on outputs
            if section_halves_match:
                inputs_modified = True
                inputs_new[input_index] = BIT_0
            # otherwise, split up sections into halves and try the next input
            sections *= 2
        if inputs_modified:
            return BitExpression(gate, *inputs_new)
        else:
            return None

    @staticmethod
    def fix_inputs(bit: Bit) -> Bit | None:
        """
        Performs analysis on the given bit to determine its effective gate and inputs, then optimizes away any inputs which have no effect on the outputs.

        :param bit: The bit to optimize.
        :return: An optimized bit, or None.
        """
        analysis = BitVectorAnalysis.for_bit(bit)
        gate_input_references = analysis.inputs()
        gate_inputs = [reference.value for reference in gate_input_references]
        gate = analysis.compute()
        return BitExpressionOptimization._fix_inputs(gate_inputs, gate)

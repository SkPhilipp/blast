from blast.analysis import BitVectorAnalysis
from blast.bit import BitMutable, BitExpression, Reference
from blast.bitvector import BitVector
from blast.optimize import BitExpressionOptimization


def test_all():
    undetermined_1 = BitMutable()
    undetermined_2 = BitMutable()
    undetermined_3 = BitMutable()
    expression = (undetermined_1 & undetermined_2) | ((undetermined_1 & undetermined_2) & undetermined_3)
    expression_bitvector = BitVector([expression])
    expression_analysis = BitVectorAnalysis(expression_bitvector)

    reconstruct_inputs = expression_analysis.inputs()
    reconstruct_gate = expression_analysis.compute()
    reconstructed = BitExpression(reconstruct_gate, *[element.value for element in reconstruct_inputs])
    optimized = BitExpressionOptimization.optimize(reconstructed)

    # verify that 'optimized' has less inputs than the original & that its inputs are references to undetermined bits
    assert len(reconstruct_inputs) == 3
    assert len(optimized.inputs()) == 2
    assert optimized.inputs() == {Reference(undetermined_1), Reference(undetermined_2)}

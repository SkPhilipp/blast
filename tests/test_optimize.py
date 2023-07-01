from blast.bit import BitMutable, Reference
from blast.optimize import BitExpressionOptimization


def test_dynamic():
    for i in range(100):
        undetermined_1 = BitMutable()
        undetermined_2 = BitMutable()
        undetermined_3 = BitMutable()
        undetermined_4 = BitMutable()

        # in this expression undetermined_3 and undetermined_4 have no actual effect on its result
        unoptimized = (undetermined_1 & undetermined_2) | ((undetermined_1 & undetermined_2) & undetermined_3 & undetermined_4)
        optimized = BitExpressionOptimization.fix_inputs(unoptimized)

        assert len(optimized.inputs()) == 2
        assert optimized.inputs() == {Reference(undetermined_1), Reference(undetermined_2)}

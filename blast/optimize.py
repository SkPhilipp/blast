from blast.bit import Bit, BitExpression, BIT_0, BIT_1


class BitExpressionOptimization(object):
    """
    Base class for optimizations of BitExpressions.
    """

    @staticmethod
    def _apply3(inputs: [Bit], computed: [int]) -> Bit | None:
        """
        Apply this optimization to a 3-input expression.
        :param inputs: The inputs to the gate.
        :param computed: The computed outputs of the expression.
        :return: An optimized expression, or None.
        """
        if len(inputs) != 3:
            raise ValueError("Expected 3 inputs, got %d" % len(inputs))
        if len(computed) != 8:
            raise ValueError("Expected 8 outputs, got %d" % len(computed))
        if computed[0] == computed[4] and computed[1] == computed[5] and computed[2] == computed[6] and computed[3] == computed[7]:
            return BitExpression(computed[0:4], inputs[0], inputs[1])
        if computed[0] == computed[2] and computed[1] == computed[3] and computed[4] == computed[6] and computed[5] == computed[7]:
            return BitExpression(computed[0:2] + computed[4:6], inputs[0], inputs[2])
        if computed[0] == computed[1] and computed[2] == computed[3] and computed[4] == computed[5] and computed[6] == computed[7]:
            return BitExpression(computed[0:1] + computed[2:3] + computed[4:5] + computed[6:7], inputs[1], inputs[2])
        return None

    @staticmethod
    def _apply2(inputs: [Bit], computed: [int]) -> Bit | None:
        """
        Apply this optimization to a 2-input expression.
        :param inputs: The inputs to the gate.
        :param computed: The computed outputs of the expression.
        :return: An optimized expression, or None.
        """
        if len(inputs) != 2:
            raise ValueError("Expected 2 inputs, got %d" % len(inputs))
        if len(computed) != 4:
            raise ValueError("Expected 4 outputs, got %d" % len(computed))
        if computed[0] == computed[2] and computed[1] == computed[3]:
            return BitExpression(computed[0:2], inputs[0])
        if computed[0] == computed[1] and computed[2] == computed[3]:
            return BitExpression(computed[0:1] + computed[2:3], inputs[1])
        return None

    @staticmethod
    def _apply1(inputs: [Bit], computed: [int]) -> Bit | None:
        """
        Apply this optimization to a 1-input expression.
        :param inputs: The inputs to the gate.
        :param computed: The computed outputs of the expression.
        :return: A constant bit, or None.
        """
        if len(inputs) != 1:
            raise ValueError("Expected 1 input, got %d" % len(inputs))
        if len(computed) != 2:
            raise ValueError("Expected 2 outputs, got %d" % len(computed))
        if computed[0] == 0 and computed[1] == 0:
            return BIT_0
        if computed[0] == 1 and computed[1] == 1:
            return BIT_1
        return None

    @staticmethod
    def _optimize(inputs: [Bit], computed: [int]) -> Bit | None:
        """
        Apply this optimization to an expression.
        :param inputs: The inputs to the gate.
        :param computed: The computed outputs of the expression.
        :return: An optimized expression, or None.
        """
        if len(inputs) == 3 and len(computed) == 8:
            return BitExpressionOptimization._apply3(inputs, computed)
        if len(inputs) == 2 and len(computed) == 4:
            return BitExpressionOptimization._apply2(inputs, computed)
        if len(inputs) == 1 and len(computed) == 2:
            return BitExpressionOptimization._apply1(inputs, computed)
        return None

    @staticmethod
    def optimize(bit: Bit) -> Bit:
        """
        Apply optimizations repeatedly to an expression until no further optimizations are possible.
        :param bit: The expression to optimize.
        :return: An optimized expression, or None.
        """
        best_optimized = bit
        while isinstance(best_optimized, BitExpression):
            optimized = BitExpressionOptimization._optimize(best_optimized.dependencies(), best_optimized.gate)
            if optimized is None:
                break
            best_optimized = optimized
        return best_optimized

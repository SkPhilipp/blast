import enum


class ExpressionType(enum.Enum):
    """
    Contains bit-vector operations that can be used to build a symbolic expression.

    Noteworthy is that all 15 possible output matrices for 2-bit inputs are also enums.
    For example, BITWISE_AND is tagged with 1 (0b0001) as its table for 2 input bits looks as follows:

    | in 0 | in 1 | out |
    |------|------|-----|
    |    0 |    0 |   0 |
    |    0 |    1 |   0 |
    |    1 |    0 |   0 |
    |    1 |    1 |   1 |

    Enums 0 through 15 represent one of the 16 unique tables for 2-bit inputs.
    """

    # [0, 0, 0, 0] (No dependencies.)
    CONSTANT_0 = 0

    # [0, 0, 0, 1] (Depends on both bits.)
    AND = IS_ONE = 1

    # [0, 0, 1, 0] (Depends on both bits.)
    GREATER_THAN = 2

    # [0, 0, 1, 1] (Depends on the first bit.)
    # Effectively an operation to get the first bit.
    BITWISE_UNKNOWN_3 = 3

    # [0, 1, 0, 0] (Depends on both bits.)
    LESS_THAN = 4

    # [0, 1, 0, 1] (Depends on the first bit.)
    # Effectively an operation to get the second bit.
    BITWISE_UNKNOWN_5 = 5

    # [0, 1, 1, 0] (Depends on both input bits; or rather, the relation between them.)
    XOR = NOT_EQUALS = 6

    # [0, 1, 1, 1] (Depends on both input bits.)
    OR = BITWISE_NOT_ZERO = 7

    # [1, 0, 0, 0] (Depends on both input bits.)
    BITWISE_EQUALS_ZERO = 8

    # [1, 0, 0, 1] (Depends on both input bits; or rather, the relation between them.)
    EQUALS = 9

    # [1, 0, 1, 0] (Depends on the second bit.)
    # Effectively a "not second bit" operation.
    BITWISE_UNKNOWN_10 = 10

    # [1, 0, 1, 1] (Depends on both input bits.)
    GREATER_THAN_OR_EQUALS = 11

    # [1, 1, 0, 0] (Depends on the first bit.)
    # Effectively a "not first bit" operation.
    BITWISE_UNKNOWN_12 = 12

    # [1, 1, 0, 1] (Depends on both input bits.)
    LESS_THAN_OR_EQUALS = 13

    # [1, 1, 1, 0] (Depends on both input bits.)
    BITWISE_NAND = BITWISE_NOT_ONE = 14

    # [1, 1, 1, 1] (No dependencies.)
    CONSTANT_1 = 15

    # Operations involving one input.
    BITWISE_IDENTITY = 1000
    INVERT = 1001
    LEFT_SHIFT = 1002
    RIGHT_SHIFT = 1003
    SELECT_RANGE = 1004
    SELECT_EXTEND = 1005

    # Operations involving two inputs.
    ADD = 2000

    def __str__(self):
        mapping = {
            ExpressionType.CONSTANT_0: "set0",
            ExpressionType.AND: "and",
            ExpressionType.GREATER_THAN: "gt",
            ExpressionType.BITWISE_UNKNOWN_3: "unknown3",
            ExpressionType.LESS_THAN: "lt",
            ExpressionType.BITWISE_UNKNOWN_5: "unknown5",
            ExpressionType.XOR: "xor",
            ExpressionType.NOT_EQUALS: "ne",
            ExpressionType.OR: "or",
            ExpressionType.BITWISE_NOT_ZERO: "not0",
            ExpressionType.BITWISE_EQUALS_ZERO: "is0",
            ExpressionType.EQUALS: "eq",
            ExpressionType.BITWISE_UNKNOWN_10: "unknown10",
            ExpressionType.GREATER_THAN_OR_EQUALS: "gte",
            ExpressionType.BITWISE_UNKNOWN_12: "unknown12",
            ExpressionType.LESS_THAN_OR_EQUALS: "lte",
            ExpressionType.BITWISE_NAND: "nand",
            ExpressionType.BITWISE_NOT_ONE: "not1",
            ExpressionType.CONSTANT_1: "set1",
            ExpressionType.BITWISE_IDENTITY: "identity",
            ExpressionType.INVERT: "not",
            ExpressionType.LEFT_SHIFT: "lshift",
            ExpressionType.RIGHT_SHIFT: "rshift",
            ExpressionType.SELECT_RANGE: "range",
            ExpressionType.SELECT_EXTEND: "extend",
            ExpressionType.ADD: "add",
        }
        return mapping[self]


class ExpressionVariable(object):
    def __init__(self, name: str, length: int):
        self._name: str = name
        self._length: int = length

    def __len__(self):
        return self._length

    def __str__(self):
        return self._name


class Expression(object):
    """
    Expression overloads Python operators allowing for easy construction of expressions on any type of input.

    Generally, these inputs would be bit vectors.
    """

    def __init__(self, expression_type: ExpressionType, bit_inputs: [], bit_output_offset: int = 0, bit_output_length: int = None):
        """
        :param expression_type: A value from the ExpressionType enum.
        :param bit_inputs: A list of bit vectors.
        :param bit_output_offset: When positive, the output is a subset of the input, starting at the given offset.
                                  When negative, the output is padded with zeroes to the left by the given offset.
        :param bit_output_length: Ignored when extending by a negative offset.
                                  If None, the length is inferred from the longest input.
                                  When shorter than the longest input, the output is truncated.
                                  When longer than the longest input, the output is padded with zeros by the given length.
        """
        self._type: ExpressionType = expression_type
        self._inputs: [] = bit_inputs
        self._output_offset: int = bit_output_offset
        if self._output_offset < 0:
            self._output_length: int = max([len(bit_input) for bit_input in bit_inputs]) - self._output_offset
        else:
            self._output_length: int = bit_output_length if bit_output_length is not None else max([len(bit_input) for bit_input in bit_inputs])
        if self._output_length < 0:
            raise ValueError("Output length must be non-negative.")

    @staticmethod
    def of(value: []):
        return Expression(ExpressionType.BITWISE_IDENTITY, [value])

    def __add__(self, other):
        return Expression(ExpressionType.ADD, [self, other])

    def __xor__(self, other):
        return Expression(ExpressionType.XOR, [self, other])

    def __and__(self, other):
        return Expression(ExpressionType.AND, [self, other])

    def __or__(self, other):
        return Expression(ExpressionType.OR, [self, other])

    def __invert__(self):
        return Expression(ExpressionType.INVERT, [self])

    def __eq__(self, other):
        return Expression(ExpressionType.EQUALS, [self, other])

    def __ne__(self, other):
        return Expression(ExpressionType.NOT_EQUALS, [self, other])

    def __lt__(self, other):
        return Expression(ExpressionType.LESS_THAN, [self, other])

    def __gt__(self, other):
        return Expression(ExpressionType.GREATER_THAN, [self, other])

    def __le__(self, other):
        return Expression(ExpressionType.LESS_THAN_OR_EQUALS, [self, other])

    def __ge__(self, other):
        return Expression(ExpressionType.GREATER_THAN_OR_EQUALS, [self, other])

    def __lshift__(self, other):
        return Expression(ExpressionType.LEFT_SHIFT, [self, other])

    def __rshift__(self, other):
        return Expression(ExpressionType.RIGHT_SHIFT, [self, other])

    def __getitem__(self, item):
        """
        An implementation of the Python slice operator allowing for both extending and truncating the expression.
        :param item:
        :return:
        """
        # ensure this method is invoked with a slice
        if isinstance(item, int):
            return self.__getitem__(slice(item, item + 1))

        # when the item is any other type
        if not isinstance(item, slice):
            raise TypeError(f"Invalid argument type {type(item)} for __getitem__")

        # return self when the slice is an exact match to the output
        if item.start == 0 and item.stop == self._output_length:
            return self

        # extend when the slice is out of bounds at the start
        if item.start < 0:
            extended = Expression(ExpressionType.SELECT_EXTEND, [self], item.start)
            return extended.__getitem__(slice(0, item.stop - item.start))

        # extend when the slice is out of bounds at the end
        if item.stop > self._output_length:
            extended = Expression(ExpressionType.SELECT_EXTEND, [self], 0, item.stop)
            return extended.__getitem__(slice(item.start, self._output_length))

        # select a range when the slice is within bounds
        return Expression(ExpressionType.SELECT_RANGE, [self], item.start, item.stop - item.start)

    def __len__(self):
        return self._output_length

    def __str__(self):
        return self._to_string()

    def _to_string(self):
        return f"{self._type}({', '.join([str(bit_input) for bit_input in self._inputs])})"

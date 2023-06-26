class Reference(object):
    """
    A class referencing an object, implements equality and hash using only the id of the referenced object.
    """

    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return isinstance(other, Reference) and id(self.value) == id(other.value)

    def __lt__(self, other):
        return isinstance(other, Reference) and id(self.value) < id(other.value)

    def __hash__(self):
        return id(self.value)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f"Reference(@{id(self.value)})"


class Bit(object):
    """
    Abstract base class representing a symbolic bit which is either unknown, a 1-bit value, or an expression.
    This class overloads operators on which some data structures rely and as such should be wrapped by a Reference in order to be used in dicts and sets.
    """

    def is_concrete(self) -> bool:
        """
        Returns true if the read result of the transform is expected to be concrete.
        """
        raise NotImplementedError()

    def inputs(self) -> set[Reference]:
        """
        Returns a set of Bit dependencies which must be assigned a value before this Bit can be resolved.
        """
        raise NotImplementedError()

    def __int__(self) -> int:
        """
        Applies the transform on any concrete local inputs and returns a value.

        :type: int
        """
        raise NotImplementedError()

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        raise NotImplementedError()

    def __invert__(self) -> 'Bit':
        return BitExpression(BitExpression.MAPPING_1_NOT, self)

    def __xor__(self, other) -> 'Bit':
        return BitExpression(BitExpression.MAPPING_2_XOR, self, other)

    def __and__(self, other) -> 'Bit':
        return BitExpression(BitExpression.MAPPING_2_AND, self, other)

    def __or__(self, other) -> 'Bit':
        return BitExpression(BitExpression.MAPPING_2_OR, self, other)

    def __add__(self, other) -> 'Bit':
        return BitExpression(BitExpression.MAPPING_2_ADD, self, other)

    def __lt__(self, other) -> 'Bit':
        return BitExpression(BitExpression.MAPPING_2_LESS_THAN, self, other)

    def __le__(self, other) -> 'Bit':
        return BitExpression(BitExpression.MAPPING_2_LESS_THAN_OR_EQUALS, self, other)

    def __gt__(self, other) -> 'Bit':
        return BitExpression(BitExpression.MAPPING_2_GREATER_THAN, self, other)

    def __ge__(self, other) -> 'Bit':
        return BitExpression(BitExpression.MAPPING_2_GREATER_THAN_OR_EQUALS, self, other)

    def __eq__(self, other) -> 'Bit':
        return BitExpression(BitExpression.MAPPING_2_EQUALS, self, other)

    def __ne__(self, other) -> 'Bit':
        return BitExpression(BitExpression.MAPPING_2_NOT_EQUALS, self, other)

    @staticmethod
    def add(a: 'Bit', b: 'Bit', carry: 'Bit') -> ('Bit', 'Bit'):
        """
        Adds two bits and a carry bit, returning their sum and the carry bit of the sum.
        :param a
        :param b
        :param carry
        :return:
        """
        total = BitExpression(BitExpression.MAPPING_3_ADD, a, b, carry)
        carry = BitExpression(BitExpression.MAPPING_3_ADD_CARRY, a, b, carry)
        return total, carry


class BitImmutable(Bit):
    """
    An implementation of a symbolic bit which is immutable and always has a value.
    """

    def __init__(self, value):
        self._value = value
        """
        Concrete value of this Bit.

        :type: int
        """

    def is_concrete(self):
        return True

    def inputs(self):
        return {}

    def __int__(self):
        return self._value

    def __repr__(self):
        return str(self._value)


BIT_0 = BitImmutable(0)
BIT_1 = BitImmutable(1)


class BitMutable(Bit):
    """
    An implementation of a symbolic bit which is mutable and may be assigned a value.
    """

    def __init__(self, value: int | None = None):
        self._value = None
        """
        Concrete value of this Bit, if any.
        :type: int|None
        """
        self.assign(value)

    def assign(self, value: int | None):
        if value not in (0, 1, None):
            raise ValueError("Value must be 0, 1 or None.")
        self._value = value

    def is_concrete(self):
        return self._value is not None

    def inputs(self):
        return {Reference(self)}

    def __int__(self):
        return self._value

    def __repr__(self):
        if self._value is None:
            return "?"
        else:
            return str(self._value)


class BitExpression(Bit):
    """
    An implementation of a symbolic bit mapping its inputs through a list of outputs. For example;
    - 1-bit NOT as a BitExpression would be represented by outputs [1, 0]. (for inputs 0b0, 0b1 respectively)
    - 2-bit AND as a BitExpression would be represented by outputs [0, 0, 0, 1]. (for inputs 0b00, 0b01, 0b10, 0b11 respectively)
    """

    def __init__(self, outputs: [int], *dependencies: Bit):
        self.outputs: [int] = outputs
        """
        List of outputs for this.
        """
        self.dependencies: [Bit] = dependencies

    def inputs(self):
        inputs = set()
        for dependency in self.dependencies:
            inputs.update(dependency.inputs())
        return inputs

    def is_concrete(self):
        for dependency in self.dependencies:
            if not dependency.is_concrete():
                return False
        return True

    def __int__(self):
        index = 0
        for dependency in reversed(self.dependencies):
            index <<= 1
            index |= int(dependency) & 1
        return self.outputs[index]

    def __repr__(self):
        output_int = 0
        for output in self.outputs:
            output_int <<= 1
            output_int |= output & 1
        return "({})".format(f" {output_int} ".join(repr(dependency) for dependency in self.dependencies))


BitExpression.MAPPING_1_NOT = [1, 0]
BitExpression.MAPPING_1_CONSTANT_ZERO = [0, 0]
BitExpression.MAPPING_2_CONSTANT_ZERO = [0, 0, 0, 0]
BitExpression.MAPPING_2_AND = [0, 0, 0, 1]
BitExpression.MAPPING_2_GREATER_THAN = [0, 1, 0, 0]
BitExpression.MAPPING_2_LESS_THAN = [0, 0, 1, 0]
BitExpression.MAPPING_2_XOR = BitExpression.MAPPING_2_ADD = BitExpression.MAPPING_2_NOT_EQUALS = [0, 1, 1, 0]
BitExpression.MAPPING_2_OR = [0, 1, 1, 1]
BitExpression.MAPPING_2_EQUALS_ZERO = [1, 0, 0, 0]
BitExpression.MAPPING_2_EQUALS = [1, 0, 0, 1]
BitExpression.MAPPING_2_LESS_THAN_OR_EQUALS = [1, 0, 1, 1]
BitExpression.MAPPING_2_GREATER_THAN_OR_EQUALS = [1, 1, 0, 1]
BitExpression.MAPPING_2_NAND = [1, 1, 1, 0]
BitExpression.MAPPING_2_CONSTANT_ONE = [1, 1, 1, 1]
BitExpression.MAPPING_3_ADD = [0, 1, 1, 0, 1, 0, 0, 1]
BitExpression.MAPPING_3_ADD_CARRY = [0, 0, 0, 1, 0, 1, 1, 1]

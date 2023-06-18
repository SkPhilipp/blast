class SymbolicBit(object):
    """
    Abstract base class for symbolic bits.
    A symbolic bit is a bit which either has a concrete value or is an expression of other symbolic bits.
    """

    def is_concrete(self):
        """
        Returns true if the read result of the transform is expected to be concrete.
        """
        raise NotImplementedError()

    def complexity(self):
        """
        Returns an estimated and arbitrary complexity of the bit.
        :return:
        """
        raise NotImplementedError()

    def simplify(self):
        """
        Returns a simplified form of the bit, if possible.
        """
        return self

    def inputs(self):
        """
        Returns a set of all symbolic bit dependency variables required to resolve this symbolic bit.
        """
        raise NotImplementedError()

    def __int__(self):
        """
        Applies the transform on any concrete local inputs and returns a value.

        :type: int
        """
        raise NotImplementedError()

    def __str__(self):
        return repr(self)

    def __repr__(self):
        raise NotImplementedError()

    def __invert__(self):
        return SymbolicBitExpressionNot(self)

    def __xor__(self, other):
        return SymbolicBitExpressionXor(self, other)

    def __and__(self, other):
        return SymbolicBitExpressionAnd(self, other)

    def __or__(self, other):
        return SymbolicBitExpressionOr(self, other)

    def __add__(self, other):
        return SymbolicBitExpressionAdd(self, other)

    def __lt__(self, other):
        """
        Less-than implementation to allow sorting of symbolic bits.

        :param other:
        :return:
        """
        return id(self) < id(other)

    def __eq__(self, other):
        """
        Base equality implementation.

        :param other:
        :return:
        """
        return id(self) == id(other)

    @staticmethod
    def add(a, b, carry):
        """
        Adds two bits and a carry bit, returning a tuple of the sum and the carry bit.
        :param a:SymbolicBit
        :param b:SymbolicBit
        :param carry:SymbolicBit
        :return:
        """
        total = SymbolicBitExpressionAdd(a, b, carry)
        total_carry = SymbolicBitExpressionAddCarry(a, b, carry)
        return total, total_carry


class SymbolicBitDynamic(SymbolicBit):
    """
    A symbolic bit whose value may both change over time, and is not always known.
    """

    def __init__(self, value=None):
        self._value = None
        """
        Concrete value of this symbolic bit, if any.

        :type: int|None
        """
        self.assign(value)

    def assign(self, value):
        if value not in (0, 1, None):
            raise ValueError("Value must be 0, 1 or None.")
        self._value = value

    def is_concrete(self):
        return self._value is not None

    def complexity(self):
        return 2 if self._value is None else 1

    def inputs(self):
        if self._value is None:
            return {self}
        else:
            return set()

    def __int__(self):
        return self._value

    def __repr__(self):
        if self._value is None:
            return "?"
        else:
            return str(self._value)

    def __eq__(self, other):
        """
        :param other:
        :return:
        """
        return id(self) == id(other) or isinstance(other, SymbolicBitDynamic) and self._value == other._value

    def __hash__(self):
        return id(self)


BIT_0 = SymbolicBitDynamic(0)
BIT_1 = SymbolicBitDynamic(1)


class SymbolicBitExpression(SymbolicBit):
    _call_id_complexity = 1
    _call_id_simplify = 1
    """
    Abstract base class for symbolic bit expressions.
    A symbolic bit expression is a symbolic bit which is a transform of other symbolic bits.
    """

    def __init__(self, *dependencies):
        self._cached_complexity = None
        self._cached_complexity_id = 0
        self._cached_simplify = None
        self._cached_simplify_id = 0
        self.dependencies = list(dependencies)
        """
        Dependency symbolic bits of this symbolic bit.

        :type: list[SymbolicBit]
        """

    def inputs(self):
        inputs = set()
        for dependency in self.dependencies:
            inputs.update(dependency.inputs())
        return inputs

    def simplify_dependencies(self):
        """
        Replaces the symbolic bits in the dependency tree with their most simplified version.
        """
        for i in range(len(self.dependencies)):
            if isinstance(self.dependencies[i], SymbolicBitExpression):
                self.dependencies[i] = self.dependencies[i].simplify()
        self.dependencies.sort()

    @staticmethod
    def simplify_cache_clear():
        SymbolicBitExpression._call_id_simplify += 1

    def simplify_concrete(self):
        """
        Returns a (concrete) dynamic symbolic bit when this expression is concrete.
        """
        if self.is_concrete():
            value = int(self)
            if value == 1:
                return BIT_1
            if value == 0:
                return BIT_0
        return self

    def simplify_local(self):
        """
        Simplifies this expression locally, without simplifying the dependency tree.

        :return: SymbolicBitExpression|None
        """
        pass

    def simplify(self):
        """
        Replaces the symbolic bits in the dependency tree with their most simplified version.
        Returns a simplified form of the bit, if possible.

        The result is cached until SymbolicBitExpression.simplify_cache_clear() is invoked.
        """
        if SymbolicBitExpression._call_id_simplify == self._cached_simplify_id:
            return self._cached_simplify

        self.simplify_dependencies()
        simplification = self.simplify_local()
        if simplification is None:
            simplification = self.simplify_concrete()

        self._cached_simplify = simplification
        self._cached_simplify_id = SymbolicBitExpression._call_id_simplify

        return simplification

    def is_concrete(self):
        """
        Returns true when all dependency bits are concrete.
        :return:
        """
        for dependency in self.dependencies:
            if not dependency.is_concrete():
                return False
        return True

    @staticmethod
    def complexity_cache_clear():
        SymbolicBitExpression._call_id_complexity += 1

    def complexity(self):
        """
        Returns an estimated and arbitrary complexity of the bit.

        The result is cached until SymbolicBitExpression.complexity_cache_clear() is invoked.
        :return:
        """
        if SymbolicBitExpression._call_id_complexity == self._cached_complexity_id:
            return self._cached_complexity

        complexity = 1
        for dependency in self.dependencies:
            complexity += dependency.complexity()

        self._cached_complexity = complexity
        self._cached_complexity_id = SymbolicBitExpression._call_id_complexity

        return complexity

    def __int__(self):
        raise NotImplementedError()

    def __repr__(self):
        raise NotImplementedError()

    def __eq__(self, other):
        """
        :param other:
        :return:
        """
        if isinstance(other, SymbolicBitExpression):
            for i in range(len(self.dependencies)):
                if self.dependencies[i] != other.dependencies[i]:
                    return False
        return id(self) == id(other)


class SymbolicBitExpressionNot(SymbolicBitExpression):
    """
    A symbolic bit which is the bitwise not of another symbolic bit.
    """

    def __init__(self, bits):
        super().__init__(bits)

    def __int__(self):
        return 1 - int(self.dependencies[0])

    def simplify_local(self):
        dependency = self.dependencies[0]
        # ~(~x) = x
        if isinstance(dependency, SymbolicBitExpressionNot):
            return dependency.dependencies[0]

    def __repr__(self):
        return "(~{})".format(self.dependencies[0])


class SymbolicBitExpressionXor(SymbolicBitExpression):
    """
    A symbolic bit which is the bitwise xor of two other symbolic bits.
    """

    def __init__(self, *bits):
        super().__init__(*bits)

    def __int__(self):
        result = 0
        for dependency in self.dependencies:
            result ^= int(dependency)
        return result

    def simplify_local(self):
        # xor(..., x, x) = xor(..., 0, 0)
        for i in range(len(self.dependencies) - 1):
            if self.dependencies[i] is self.dependencies[i + 1]:
                self.dependencies[i] = BIT_0
                self.dependencies[i + 1] = BIT_0
        # xor(..., 0) = xor(...)
        self.dependencies = [dependency for dependency in self.dependencies if dependency is not BIT_0]
        # xor(x) = x
        if len(self.dependencies) == 1:
            return self.dependencies[0]

    def __repr__(self):
        return "({})".format(" ^ ".join(repr(dependency) for dependency in self.dependencies))


class SymbolicBitExpressionAnd(SymbolicBitExpression):
    """
    A symbolic bit which is the bitwise and of two other symbolic bits.
    """

    def __init__(self, *bits):
        super().__init__(*bits)

    def __int__(self):
        result = 1
        for dependency in self.dependencies:
            result &= int(dependency)
        return result

    def simplify_local(self):
        # and(..., and(...), ...) = and(..., ..., ...)
        for i in range(len(self.dependencies)):
            child = self.dependencies[i]
            if isinstance(child, SymbolicBitExpressionAnd):
                self.dependencies[i:i + 1] = child.dependencies
        # and(..., x, x) = and(..., 1, x)
        for i in range(len(self.dependencies) - 1):
            if self.dependencies[i] is self.dependencies[i + 1]:
                self.dependencies[i] = BIT_1
        # and(..., 1) = and(...)
        self.dependencies = [dependency for dependency in self.dependencies if dependency is not BIT_1]
        # and(..., 0) = 0
        if BIT_0 in self.dependencies:
            return BIT_0
        # and(x) = x
        if len(self.dependencies) == 1:
            return self.dependencies[0]
        # and() = 1
        if len(self.dependencies) == 0:
            return BIT_1

    def __repr__(self):
        return "({})".format(" & ".join(repr(dependency) for dependency in self.dependencies))


class SymbolicBitExpressionOr(SymbolicBitExpression):
    """
    A symbolic bit which is the bitwise or of two other symbolic bits.
    """

    def __init__(self, *bits):
        super().__init__(*bits)

    def __int__(self):
        result = 0
        for dependency in self.dependencies:
            result |= int(dependency)
        return result

    def simplify_local(self):
        # or(..., or(...), ...) = or(..., ..., ...)
        for i in range(len(self.dependencies)):
            child = self.dependencies[i]
            if isinstance(child, SymbolicBitExpressionOr):
                self.dependencies[i:i + 1] = child.dependencies
        # or(..., x, x) = or(..., 0, x)
        for i in range(len(self.dependencies) - 1):
            if self.dependencies[i] is self.dependencies[i + 1]:
                self.dependencies[i] = BIT_0
        # or(..., 0) = or(...)
        self.dependencies = [dependency for dependency in self.dependencies if dependency is not BIT_0]
        # or(..., 1) = 1
        if BIT_1 in self.dependencies:
            return BIT_1
        # or(x) = x
        if len(self.dependencies) == 1:
            return self.dependencies[0]
        # or() = 0
        if len(self.dependencies) == 0:
            return BIT_0

    def __repr__(self):
        return "({})".format(" | ".join(repr(dependency) for dependency in self.dependencies))


class SymbolicBitExpressionAdd(SymbolicBitExpression):
    """
    A symbolic bit which is the bitwise add of 1 to 3 symbolic bits, overflow past 1 is ignored.
    """

    def __init__(self, *bits):
        super().__init__(*bits)

    def __int__(self):
        result = 0
        for dependency in self.dependencies:
            result += int(dependency)
        return result % 2

    def simplify_local(self):
        # add(..., add(...), ...) = add(..., ..., ...)
        for i in range(len(self.dependencies)):
            child = self.dependencies[i]
            if isinstance(child, SymbolicBitExpressionAdd):
                self.dependencies[i:i + 1] = child.dependencies
        # add(..., x, x) = add(..., 0, 0)
        for i in range(len(self.dependencies) - 1):
            if self.dependencies[i] is self.dependencies[i + 1]:
                self.dependencies[i] = BIT_0
                self.dependencies[i + 1] = BIT_0
        # add(..., 0) = add(...)
        self.dependencies = [dependency for dependency in self.dependencies if dependency is not BIT_0]

    def __repr__(self):
        return "({})".format(" + ".join(repr(dependency) for dependency in self.dependencies))


class SymbolicBitExpressionAddCarry(SymbolicBitExpression):
    """
    A symbolic bit which is the carry bit of the bitwise add of 1 to 3 symbolic bits.
    """

    def __init__(self, *bits):
        super().__init__(*bits)

    def __int__(self):
        result = 0
        for dependency in self.dependencies:
            result += int(dependency)
        return result // 2

    def simplify_local(self):
        # add_carry(x, x, y) = y
        # add_carry(x, y, y) = x
        if len(self.dependencies) == 3:
            if self.dependencies[0] is self.dependencies[1]:
                return self.dependencies[2]
            if self.dependencies[1] is self.dependencies[2]:
                return self.dependencies[0]
        # add_carry(..., 0) = add_carry(...)
        self.dependencies = [dependency for dependency in self.dependencies if dependency is not BIT_0]
        # add_carry(x) = 0
        if len(self.dependencies) == 1:
            return BIT_0

    def __repr__(self):
        return "carry({})".format(" + ".join(repr(dependency) for dependency in self.dependencies))


if __name__ == "__main__":
    undetermined_1 = SymbolicBitDynamic()
    undetermined_2 = SymbolicBitDynamic()

    # fully concrete
    assert int(~BIT_0) == 1
    assert int(BIT_1 | BIT_0) == 1
    assert int(BIT_1 & BIT_1) == 1
    assert int(BIT_1 ^ BIT_0) == 1

    # one layer of indirection
    assert int((~undetermined_1 | BIT_1).simplify()) == 1
    assert int((~undetermined_1 & BIT_0).simplify()) == 0

    # minimal information
    assert int((BIT_1 | undetermined_1).simplify()) == 1
    assert int((undetermined_1 | BIT_1).simplify()) == 1
    assert int((BIT_0 & undetermined_1).simplify()) == 0
    assert int((undetermined_1 & BIT_0).simplify()) == 0

    # representation
    assert repr(BIT_0 | (BIT_1 & undetermined_1)) == "(0 | (1 & ?))"

    # inputs
    assert undetermined_1.inputs() == {undetermined_1}
    assert (~undetermined_1 | BIT_1).inputs() == {undetermined_1}
    assert (undetermined_1 | undetermined_2).inputs() == {undetermined_1, undetermined_2}

    print("OK")

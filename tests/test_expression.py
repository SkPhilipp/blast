from blast.expression import Expression, ExpressionType, ExpressionVariable


def test_constants():
    exp1 = Expression.of([0, 0, 0, 0])
    exp2 = Expression(ExpressionType.INVERT, [[1, 1, 0, 0]])
    exp3 = Expression(ExpressionType.EQUALS, [exp1, exp2])
    assert len(exp1) == 4
    assert len(exp2) == 4
    assert len(exp3) == 4
    assert str(exp3) == "eq(identity([0, 0, 0, 0]), not([1, 1, 0, 0]))"


def test_variables():
    var1 = Expression.of(ExpressionVariable("variable1", 4))
    var2 = Expression.of(ExpressionVariable("variable2", 4))
    assert len(var1) == 4
    assert len(var2) == 4

    exp1 = Expression(ExpressionType.INVERT, [var1])
    exp2 = Expression(ExpressionType.EQUALS, [exp1, var2])
    assert len(exp1) == 4
    assert len(exp2) == 4
    assert str(exp2) == "eq(not(identity(variable1)), identity(variable2))"

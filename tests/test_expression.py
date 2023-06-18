from blast.expression import Expression, ExpressionType, ExpressionVariable


def test_constants():
    exp1 = Expression.of([0, 0, 0, 0])
    exp2 = Expression(ExpressionType.INVERT, [[1, 1, 0, 0]])
    exp3 = Expression(ExpressionType.EQUALS, [exp1, exp2])
    print(exp3[-2:2][2:4])
    print(len(exp1))
    print(len(exp2))
    print(len(exp3))
    assert exp1 == exp2


def test_variables():
    var1 = Expression.of(ExpressionVariable("variable1", 4))
    var2 = Expression.of(ExpressionVariable("variable2", 4))
    exp1 = Expression(ExpressionType.INVERT, [var1])
    exp2 = Expression(ExpressionType.EQUALS, [exp1, var2])
    print(exp2[-2:2][2:4])
    print(len(exp1))
    print(len(exp2))
    print(len(var1))
    print(len(var2))

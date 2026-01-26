from std import *

def test_std_calc():
    # Division by zero should return 0
    assert evaluate_expression("10/0") == 0

    # Not allowed characters should be caught by validation
    assert evaluate_expression('a+b') == 0

    # NULL input should return 0
    assert evaluate_expression("") == 0

    # Weird symbols should be caught by validation
    assert evaluate_expression("🙄🙄🙄🙄") == 0

    # Syntax error should be caught by validation
    assert evaluate_expression("-/*-+/+-*+*-/-3+/") == 0

    # Basic functionality of std calc should be correct
    assert evaluate_expression("15*(6+3-1)+215-(31*(4/35)**16)//733%648") == 335.0

    # Multi decimal, Syntax error should be caught by validation
    assert evaluate_expression("5...56.67.5.443.") == 0

    # Decimal precision, if Floating point error should be caught by validation
    assert evaluate_expression("0.1 + 0.2") == 0.3

    # Decimal precision test2, should return precise results
    assert evaluate_expression("0.2222**22") == 4.24980693916337e-15

    # Overflow of result should be caught by except block in eval_exp
    assert evaluate_expression("1000000000.0**1000") == 0

    # Unbalanced 15 layer Parenthesis check, should return 0
    assert evaluate_expression(""")))))))))))))))1+1((((((((((((((""") == 0
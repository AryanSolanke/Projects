from math import *

def errmsg():
    print("Error: Invalid input.")

def exp_input():
    exp = input("Enter expression(eg. 2+3*4): ")
    return exp

def validate_exp(exp):
    if exp.count('(') != exp.count(')'):
        print("Error: Unbalanced paranthesis")
        return 0
    if not exp.strip():
        print("No input given")
        return 0
    allowed_chars = "0123456789+-*/%(). "
    for char in exp:
        if char not in allowed_chars:
            print("Error: characters not allowed")
            return 0
    return 1

def evaluate_expression(exp):
    if validate_exp(exp):
        try:
            return float(f"{eval(exp):.15g}")
        except (SyntaxError, ZeroDivisionError, TypeError, OverflowError):
            errmsg()
            return 0
    else:
        return 0
        
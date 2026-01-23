from math import *

def errmsg():
    print("Error: Invalid input.")

def evaluate_expression():
    try:
        user_input = input("Enter expression(eg. 2+3*4): ")
        for char in user_input:
            if char.isalpha():
                errmsg()
                return None
        result = eval(user_input)
        return result
    except(ValueError, SyntaxError, ZeroDivisionError):
        errmsg()
        return None
    except (KeyboardInterrupt, EOFError):
        print("\nOperation cancelled by user")
        return None

def get_angle():
    try:
        angle = float(input("Enter angle(degrees): "))
        return angle
    except (ValueError, SyntaxError):
        errmsg()

def sine(angle):
    return sin(radians(angle))

def cosine(angle):
    return cos(radians(angle))

def tangent(angle):
    return tan(radians(angle))

def cot(angle):
    return 1/tan(radians(angle))

def sec(angle):
    return 1/cos(radians(angle))

def cosec(angle):
    return 1/sin(radians(angle))

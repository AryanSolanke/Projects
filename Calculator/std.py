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
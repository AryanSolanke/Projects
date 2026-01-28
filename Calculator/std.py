from math import *

def record_history_std_calc(exp, result):
    try: 
        f1 = open("std_calc_history_file.txt", 'a', encoding="utf-8")
        f1.write(f"{exp} = {result}\n")
        f1.close()
    except FileNotFoundError:
        print("Failed to record history")
    except Exception:
        errmsg()

def display_hist_std_calc():
    try:
        f1 = open("std_calc_history_file.txt", 'r', encoding="utf-8")
        history = f1.readlines()
        f1.close()
        print("History:")
        for history_val in history:
            print(history_val, end="")
    except FileNotFoundError:
        print("Failed to display history")
    except Exception:
        errmsg()

def clear_hist_std_calc():
    try:
        f = open("std_calc_history_file.txt", 'w', encoding="utf-8")
        f.write("")
        f.close()
        print("History cleared successfully!")
    except FileNotFoundError:
        print("Failed to clear history")
    except Exception:
        errmsg()

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
            result = float(f"{eval(exp):.15g}")
            record_history_std_calc(exp, result)
        except (SyntaxError, ZeroDivisionError, TypeError, OverflowError):
            errmsg()
            return 0
    else:
        return 0
        
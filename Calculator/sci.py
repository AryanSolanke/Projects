from math import *
from std import errmsg

def get_val():
    try:
        val = float(input())
        return val
    except (ValueError, SyntaxError, TypeError):
        errmsg()
        return None

def display_hist_sci_calc():
    try:
        with open("sci_calc_history_file.txt", 'r', encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                print("\nHistory is currently empty.")
            else:
                print("\n--- Scientific Calculation History ---")
                print(content)
    except FileNotFoundError:
        print("\nNo history file found. Perform a calculation first!")
    except Exception as e:
        print(f"Error reading history: {e}")

def record_history_sci_calc(name, val, answer):
    try:
        with open("sci_calc_history_file.txt", 'a', encoding="utf-8") as f:
            f.write(f"{name}({val}) = {answer}\n")
    except Exception as e:
        print(f"File Error: Could not record history. ({e})")

def clear_hist_sci_calc():
    try:
        with open("sci_calc_history_file.txt", 'w', encoding="utf-8") as f:
            pass 
        print("Scientific history cleared successfully!")
    except Exception as e:
        print(f"Could not clear history: {e}")

def validate_subOpNum(sub_op_num):
        match sub_op_num:
            case 1|2|3|4|5|6:
                return 1
            case _:
                errmsg()
                return 0
            
def frmt_ans(result):
    return f"{result:.9g}"

def print_eval(name, val, func):
    result = frmt_ans(func(val))
    record_history_sci_calc(name, val, result)
    return f"{name}({val}) = {result}"

def validate_and_eval(op_num, sub_op_num, name, func, val):
    """
    Validates input domains and executes scientific calculations.
    
    Args:
        op_num (int): Category of function (Trigo, Hyperbolic, etc.)
        sub_op_num (int): Specific function identifier within category.
        name (str): Display name of the function.
        func (callable): The mathematical function to execute.
        val (float): The input value/angle.
        
    Returns:
        str: Formatted result string or a descriptive error message.
    """
    try:
        # Category 1: Standard Trigonometric Functions
        # Handles periodicity and undefined points (asymptotes)
        if op_num == 1:
            # Undefined where sin(x) = 0: cot(x), cosec(x)
            if sub_op_num in [4, 6] and isclose(val % 180, 0, abs_tol=1e-9):
                return "Error: Division by zero (Asymptote at n*180°)"
            # Undefined where cos(x) = 0: tan(x), sec(x)
            if sub_op_num in [3, 5] and isclose(val % 180, 90, abs_tol=1e-9):
                return "Error: Division by zero (Asymptote at n*180° + 90°)"

        # Category 2: Hyperbolic Functions
        elif op_num == 2:
            # coth(0) and cosech(0) are undefined
            if sub_op_num in [4, 6] and val == 0:
                return "Error: Division by zero (Undefined at x=0)"

        # Category 3: Inverse Trigonometric Functions
        elif op_num == 3:
            # Domain check for arcsin and arccos
            if sub_op_num in [1, 2] and (val < -1 or val > 1):
                return "Domain Error: Input x must satisfy |x| <= 1"
            # Domain check for arcsec and arccosec
            if sub_op_num in [5, 6] and (-1 < val < 1):
                return "Domain Error: Input x must satisfy |x| >= 1"
            # Special case: cot⁻¹(0) is traditionally defined as 90°
            if sub_op_num == 4 and val == 0:
                return f"{name}({val}) = 90"

        # Category 4: Inverse Hyperbolic Functions
        elif op_num == 4:
            if sub_op_num == 2 and val < 1: 
                return "Domain Error: acosh(x) requires x >= 1"
            if sub_op_num == 3 and (val <= -1 or val >= 1): 
                return "Domain Error: atanh(x) requires x in open interval (-1, 1)"
            if sub_op_num == 4 and (-1 <= val <= 1): 
                return "Domain Error: acoth(x) requires x outside closed interval [-1, 1]"
            if sub_op_num == 5 and (val <= 0 or val > 1): 
                return "Domain Error: asech(x) requires x in range (0, 1]"
            if sub_op_num == 6 and val == 0: 
                return "Domain Error: acosech(x) is undefined at x=0"

        # Execution Phase: Validated inputs proceed to calculation
        return print_eval(name, val, func)

    except (ValueError, ArithmeticError) as e:
        return f"Math Error: {e}"
    except Exception as e:
        # Catch unexpected runtime exceptions (e.g., NameError, TypeError)
        return f"System Error: {type(e).__name__}"

def eval_trigo_func(key):
    if key in trigo_funcs:
        op_num, sub_op_num = key
        name, func = trigo_funcs[key]
        print("Enter angle: ", end='')
        val = get_val()
        if val!=None:
            answer = validate_and_eval(op_num, sub_op_num, name, func, val)
            print(answer)
    else:
        errmsg()

####Normal trigo functions
def sine(angle): return sin(radians(angle))
def cosine(angle): return cos(radians(angle))
def tangent(angle): return tan(radians(angle))
def cot(angle): return cos(radians(angle))/sin(radians(angle))
def sec(angle): return 1/cos(radians(angle))
def cosec(angle): return 1/sin(radians(angle))

####Inverse of Normal trigo functions
def sine_inv(val): return degrees(asin(val))
def cosine_inv(val): return degrees(acos(val))
def tangent_inv(val): return degrees(atan(val))
def cot_inv(val): return degrees(atan(1/val))
def sec_inv(val): return degrees(acos(1/val))
def cosec_inv(val): return degrees(asin(1/val))

####Hyperbolic functions
def sineh(val): return sinh(val)
def cosineh(val): return cosh(val)
def tangenth(val): return tanh(val)
def coth(val): return cosh(val)/sineh(val)
def sech(val): return 1/cosh(val)
def cosech(val): return 1/sinh(val)

####Inverse Hyperbolic functions
def sineh_inv(val): return asinh(val)
def cosineh_inv(val): return acosh(val)
def tangenth_inv(val): return atanh(val)
def coth_inv(val): return 0.5 * log((val + 1) / (val - 1))
def sech_inv(val): return acosh(1/val)
def cosech_inv(val): return asinh(1/val)

trigo_funcs = {
    (1, 1): ("sin", sine),
    (1, 2): ("cos", cosine),
    (1, 3): ("tan", tangent),
    (1, 4): ("cot", cot),
    (1, 5): ("sec", sec),
    (1, 6): ("cosec", cosec),

    (2, 1): ("sinh", sineh),
    (2, 2): ("cosh", cosineh),
    (2, 3): ("tanh", tangenth),
    (2, 4): ("coth", coth),
    (2, 5): ("sech", sech),
    (2, 6): ("cosech", cosech),

    (3, 1): ("sin⁻¹", sine_inv),
    (3, 2): ("cos⁻¹", cosine_inv),
    (3, 3): ("tan⁻¹", tangent_inv),
    (3, 4): ("cot⁻¹", cot_inv),
    (3, 5): ("sec⁻¹", sec_inv),
    (3, 6): ("cosec⁻¹", cosec_inv),

    (4, 1): ("sinh⁻¹", sineh_inv),
    (4, 2): ("cosh⁻¹", cosineh_inv),
    (4, 3): ("tanh⁻¹", tangenth_inv),
    (4, 4): ("coth⁻¹", coth_inv),
    (4, 5): ("sech⁻¹", sech_inv),
    (4, 6): ("cosech⁻¹", cosech_inv)
}
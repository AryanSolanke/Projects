from math import *
from std import errmsg

#Takes values for trigo functions
def get_val():
    try:
        val = float(input("Enter x: "))
        return val
    except (ValueError, SyntaxError, TypeError):
        errmsg()
        return None

def display_hist_sci_calc():
    try:
        f1 = open("sci_calc_history_file.txt", 'r', encoding="utf-8")
        history = f1.readlines()
        f1.close()
        print("History:")
        for history_val in history:
            print(history_val, end="")
    except FileNotFoundError:
        print("Failed to display history")
    except Exception:
        errmsg()

def record_history_sci_calc(name, val, answer):
    try: 
        f1 = open("sci_calc_history_file.txt", 'a', encoding="utf-8")
        f1.write(f"{name}({val}) = {answer}\n")
        f1.close()
    except FileNotFoundError:
        print("Failed to record history")
    except Exception:
        errmsg()

def clear_hist_sci_calc():
    try:
        f = open("sci_calc_history_file.txt", 'w', encoding="utf-8")
        f.write("")
        f.close()
        print("History cleared successfully!")
    except FileNotFoundError:
        print("Failed to clear history")
    except Exception:
        errmsg()

def validate_subOpNum(sub_op_num):
        match sub_op_num:
            case 1|2|3|4|5|6:
                return 1
            case _:
                errmsg()
                return 0
            
def format_answer(result):
    # Format to 14 decimal places as a string
    formatted_res = f"{result:.9f}"
    stripped_res = formatted_res.rstrip("0").rstrip(".")
    if stripped_res == "-0":
        return "0"
    return stripped_res      

def print_eval(name, val, func):
    result = format_answer(func(val))
    record_history_sci_calc(name, val, result)
    return f"{name}({val}) = {result}"

def validate_and_eval(op_num, sub_op_num, name, func, val):
    try:
        match op_num:
            case 1: # Normal trigo functions
                if (sub_op_num==4 or sub_op_num==6) and (isclose(val%180, 0) or abs(val)==0): 
                    return "Cannot divide by zero"
                elif (sub_op_num==3 or sub_op_num==5) and (isclose(val%180, 90) or abs(val)==90):
                    return "Cannot divide by zero"
                else:
                    return print_eval(name, val, func)

            case 2: # Hyperbolic functions
                if (sub_op_num == 4 or sub_op_num == 6) and val == 0:
                    return "Cannot divide by zero"
                else:
                    return print_eval(name, val, func)

            case 3: # Inverse of Normal trigo functions
                match sub_op_num:
                    case 1 | 2: # sin⁻¹, cos⁻¹
                        if val < -1 or val > 1:
                            return "Domain error: Enter value between [-1,1]"
                    case 5 | 6: # sec⁻¹, cosec⁻¹
                        if -1 < val < 1:
                            return "Domain error: Enter value which lie in |x|>=1"
                    case 4: # cot⁻¹ special case for x=0
                        if val == 0:
                            return f"{name}({val}) = 90" 
                return print_eval(name, val, func)

            case 4: # Inverse Hyperbolic functions
                match sub_op_num:
                    case 2: # cosh⁻¹
                        if val < 1: return "Domain error: Enter value greater than 1"
                    case 3: # tanh⁻¹
                        if val <= -1 or val >= 1: return "Domain error: Enter value between (-1,1)"
                    case 4: # coth⁻¹
                        if -1 <= val <= 1: return "Domain error: Enter value outside [-1,1]"
                    case 5: # sech⁻¹
                        if val <= 0 or val > 1: return "Domain error: Enter value in range (0,1]"
                    case 6: # cosech⁻¹
                        if val == 0: return "Domain error: Enter any value except 0"
                return print_eval(name, val, func)
            case _:
                errmsg()
                return 0
    except (ValueError, KeyboardInterrupt, UnboundLocalError,TypeError):
        errmsg()
        return 0

def eval_trigo_func(key):
    # if op_num==1:
    if key in trigo_funcs:
        op_num, sub_op_num = key
        name, func = trigo_funcs[key]
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
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

def validate_subOpNum(sub_op_num):
        match sub_op_num:
            case 1|2|3|4|5|6:
                return 1
            case _:
                errmsg()
                return 0
            
def print_eval(name, val, func):
    print(f"{name}({val}) = {func(val)}")

def validate_and_eval(op_num, choice, name, func, val):
    match op_num:
        case 1 | 3:
            print_eval(name, val, func)
        case 2:
            match choice:
                case 3 | 6:
                    print_eval(name, val, func)
                case 1 | 2:
                    if val<-1 or val>1:
                        print("Domain error: Enter value between [-1,1]")
                    else:
                        print_eval(name, val, func)
                case 4 | 5:
                    if (val>-1 and val<1):
                        print("Domain error: Enter value which don't lie between [-1,1]")
                    else:
                        print_eval(name, val, func)
                case _:
                    errmsg()
        case 4:
            match choice:
                case 1: print_eval(name, val, func)
                case 2:
                    if val<1:
                        print("Domain error: Enter value greater than 1")
                    else:
                        print_eval(name, val, func)
                case 3:
                    if val<-1 or val>1:
                        print("Domain error: Enter value between [-1,1]")
                    else:
                        print_eval(name, val, func)
                case 4:
                    if val<=0 or val>1:
                        print("Domain error: Enter value between (0,1]")
                    else:
                        print_eval(name, val, func)
                case 5:
                    if val==0:
                        print("Domain error: Enter any value except 0")
                    else:
                        print_eval(name, val, func)
                case 6:
                    if val<1 or val>-1:
                        print("Domain error: Enter value which don't lie between [-1,1]")
                    else:
                        print_eval(name, val, func)
                case _:
                    errmsg()
        case _:
            errmsg()

def eval_trigo_func(key):
    # if op_num==1:
    if key in trigo_funcs:
        op_num, choice = key
        name, func = trigo_funcs[key]
        val = get_val()
        if val!=None:
            validate_and_eval(op_num, choice, name, func, val)
    else:
        errmsg()

####Normal trigo functions
def sine(angle): return sin(radians(angle))
def cosine(angle): return cos(radians(angle))
def tangent(angle): return tan(radians(angle))
def cot(angle): return 1/tan(radians(angle))
def sec(angle): return 1/cos(radians(angle))
def cosec(angle): return 1/sin(radians(angle))

####Inverse Normal trigo functions
def sine_inv(val): return degrees(asin(val))
def cosine_inv(val): return degrees(acos(val))
def tangent_inv(val): return degrees(atan(val))
def cot_inv(val): return degrees(1/atan(val))
def sec_inv(val): return degrees(1/acos(val))
def cosec_inv(val): return degrees(1/asin(val))

####Hyperbolic functions
def sineh(val): return sinh(val)
def cosineh(val): return cosh(val)
def tangenth(val): return tanh(val)
def coth(val): return 1/tanh(val)
def sech(val): return 1/cosh(val)
def cosech(val): return 1/sinh(val)

####Inverse Hyperbolic functions
def sineh_inv(val): return asinh(val)
def cosineh_inv(val): return acosh(val)
def tangenth_inv(val): return atanh(val)
def coth_inv(val): return 1/atanh(val)
def sech_inv(val): return 1/acosh(val)
def cosech_inv(val): return 1/asinh(val)

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
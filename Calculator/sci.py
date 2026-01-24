from math import *
from std import errmsg

def get_angle():
    try:
        angle = float(input("Enter angle(degrees): "))
        return angle
    except (ValueError, SyntaxError, TypeError):
        errmsg()

#Takes values for inverse trigo functions
def get_val():
    try:
        val = float(input("Enter x: "))
        return val
    except (ValueError, SyntaxError, TypeError):
        errmsg()

def validate_val(op_num, choice, val):
    match op_num:
        case 1:
            return 1
        case 2:
            if (choice==1 or choice==2):
                if val<-1 or val>1:
                    print("Domain error: Enter value between [-1,1]")
                    return 0
                else:
                    return 1
            elif choice==3:
                return 1
            elif choice==4 or choice==5:
                if val>-1 or val<1:
                    print("Domain error: Enter value which don't lie between [-1,1]")
                    return 0
                else:
                    return 1
            elif choice==6:
                return 1
            else:
                errmsg()
        case 3:
            return 1
        case 4:
            if choice==1:
                return 1
            if choice==2:
                if val<1:
                    print("Domain error: Enter value greater than 1")
                    return 0
                else:
                    return 1
            elif choice==3:
                if val<-1 or val>1:
                    print("Domain error: Enter value between [-1,1]")
                    return 0
                else:
                    return 1
            elif choice==4:
                if val<=0 or val>1:
                    print("Domain error: Enter value between (0,1]")
                    return 0
                else:
                    return 1
            elif choice==5:
                if val==0:
                    print("Domain error: Enter any value except 0")
                    return 0
                else:
                    return 1
            elif choice==6:
                if val<1 or val>-1:
                    print("Domain error: Enter value which don't lie between [-1,1]")
                    return 0
                else:
                    return 1
            else:
                errmsg()
        case _:
            errmsg()

def eval_trigo_func(op_num, choice):
    if op_num==1:
        if choice in norm_trigo_funcs:
            name, func = norm_trigo_funcs[choice]
            angle = get_angle()
            print(f"{name}({angle}) = {func(angle)}")
        else:
            errmsg()
    elif op_num==2:
        if choice in hyperbolic_trigo_funcs:
            name, func = hyperbolic_trigo_funcs[choice]
            val = get_val()
            if validate_val(op_num, choice, val):
                print(f"{name}({val}) = {func(val)}")
        else:
            errmsg()
    elif op_num==3:
        if choice in inv_trigo_funcs:
            name, func = inv_trigo_funcs[choice]
            val = get_val()
            if validate_val(op_num, choice, val):
                print(f"{name}({val}) = {func(val)}")
        else:
            errmsg()
    elif op_num==4:
        if choice in inv_hyperbolic_trigo_funcs:
            name, func = inv_hyperbolic_trigo_funcs[choice]
            val = get_val()
            if validate_val(op_num, choice, val):
                print(f"{name}({val}) = {func(val)}")
        else:
            errmsg()
    else:
        errmsg()
    

####Normal trigo functions
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

####Inverse Normal trigo functions
def sine_inv(val):
    return degrees(asin(val))
def cosine_inv(val):
    return degrees(acos(val))
def tangent_inv(val):
    return degrees(atan(val))
def cot_inv(val):
    return degrees(1/atan(val))
def sec_inv(val):
    return degrees(1/acos(val))
def cosec_inv(val):
    return degrees(1/asin(val))

####Hyperbolic functions
def sineh(val):
    return sinh(val)
def cosineh(val):
    return cosh(val)
def tangenth(val):
    return tanh(val)
def coth(val):
    return 1/tanh(val)
def sech(val):
    return 1/cosh(val)
def cosech(val):
    return 1/sinh(val)

####Inverse Hyperbolic functions
def sineh_inv(val):
    return asinh(val)
def cosineh_inv(val):
    return acosh(val)
def tangenth_inv(val):
    return atanh(val)
def coth_inv(val):
    return 1/atanh(val)
def sech_inv(val):
    return 1/acosh(val)
def cosech_inv(val):
    return 1/asinh(val)

norm_trigo_funcs = {
    1: ("sin", sine),
    2: ("cos", cosine),
    3: ("tan", tangent), 
    4: ("cot", cot),
    5: ("sec", sec),
    6: ("cosec", cosec)
    }

hyperbolic_trigo_funcs = {
    1: ("sinh", sineh),
    2: ("cosh", cosineh),
    3: ("tanh", tangenth),
    4: ("coth", coth),
    5: ("sech", sech),
    6: ("cosech", cosech) 
    }

inv_trigo_funcs = {
    1: ("sin⁻¹", sine_inv),
    2: ("cos⁻¹", cosine_inv),
    3: ("tan⁻¹", tangent_inv),
    4: ("cot⁻¹", cot_inv),
    5: ("sec⁻¹", sec_inv),
    6: ("cosec⁻¹", cosec_inv)
}

inv_hyperbolic_trigo_funcs = {
    1: ("sinh⁻¹", sineh_inv),
    2: ("cosh⁻¹", cosineh_inv),
    3: ("tanh⁻¹", tangenth_inv),
    4: ("coth⁻¹", coth_inv),
    5: ("sech⁻¹", sech_inv),
    6: ("cosech⁻¹", cosech_inv)
}
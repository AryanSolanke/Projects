from math import *
from std import errmsg

def get_angle():
    try:
        angle = float(input("Enter angle(degrees): "))
        return angle
    except (ValueError, SyntaxError):
        errmsg()

#Takes values for inverse trigo functions
def get_val(choice):
    try:
        val = float(input("Enter angle(degrees): "))
        if val<-1 or val>1:
            errmsg()
            print("Hyperbolic functions only take values between [-1,1]")
            return None
        else:
            return val
    except (ValueError, SyntaxError):
        errmsg()

def validate_val():
    pass

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

trigo_funcs = {
    1: ("sin", sine),
    2: ("cos", cosine),
    3: ("tan", tangent), 
    4: ("cot", cot),
    5: ("sec", sec),
    6: ("cosec", cosec),

    7: ("sinh", sineh),
    8: ("cosh", cosineh),
    9: ("tanh", tangenth),
    10: ("coth", coth),
    11: ("sech", sech),
    12: ("cosech", cosech),

    13: ("sin⁻¹", sine_inv),
    14: ("cos⁻¹", cosine_inv),
    15: ("tan⁻¹", tangent_inv),
    16: ("cot⁻¹", cot_inv),
    17: ("sec⁻¹", sec_inv),
    18: ("cosec⁻¹", cosec_inv),
    
    19: ("sinh⁻¹", sineh_inv),
    20: ("cosh⁻¹", cosineh_inv),
    21: ("tanh⁻¹", tangenth_inv),
    22: ("coth⁻¹", coth_inv),
    23: ("sech⁻¹", sech_inv),
    24: ("cosech⁻¹", cosech_inv)
}


# choice = int(input("Enter choice: "))
# if choice in sci_ops:
#     name, func = sci_ops[choice]
#     val = get_angle() # or get_number()
#     print(f"{name}({val}) = {func(val)}")
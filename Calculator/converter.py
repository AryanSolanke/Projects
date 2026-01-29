from math import *
from std import errmsg
from sci import get_val, frmt_ans

def converter_menuMsg():
    print("\n|=====>Convertion Operations<=====|\n\n1. Angle.\n2. Quit Converter.")

def angle_conversion_menuMsg():
    print("\n|=====>Input choices<=====|\n\nSelect a input choice\n\n1. Degree.\n2. Radians \n3. Gradians\n4. Quit Angle Converter.")

def convert_angle(name1, func1, name2, func2, angle):
    ans1 =  f"{name1}({angle}) = {frmt_ans(func1(angle))}"
    ans2 =  f"{name2}({angle}) = {frmt_ans(func2(angle))}"
    if (ans1 or ans2)!=None:
        return ans1, ans2

def angle_converter():
    while(True):
        try:
            converter_menuMsg()
            op_num = int(input("Enter your choice: "))
            errmsg()
            match op_num:
                case 1:
                    angle_conversion_menuMsg()
                    choice = int(input("Enter your choice: "))
                    if choice in angle_conv_funcs:
                        name1, func1, name2, func2 = angle_conv_funcs[choice]
                        print(f"Enter angle in {angle_conv_choices[choice-1]}: ", end='')
                        angle = get_val()
                        if angle!=None:
                            ans1, ans2 = convert_angle(name1, func1, name2, func2, angle)
                            print(f"{ans1}\n{ans2}")
                        else:
                            print("No angle given")
                    else:
                        print("Invalid choice. select between 1-3")
                case 2:
                    print("\nAngle convertion menu closed\n")
                    break
        except (TypeError, UnboundLocalError, SyntaxError, ValueError):
            errmsg()
            continue

def to_rads(angle): return radians(angle)
def to_deg(angle): return degrees(angle)
def to_grad(angle): return (angle*200)/180

angle_conv_choices = ['Degree', 'Radians', 'Gradians']

angle_conv_funcs = {
    1: ("rad", to_rads, "grad", to_grad),
    2: ("deg", to_deg, "grad", to_grad),
    3: ("deg", to_deg, "rad", to_rads)
    }
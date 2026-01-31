from math import *
from std import errmsg
from sci import get_val, frmt_ans

def converter_menuMsg():
    print("\n|=====>Convertion Operations<=====|\n\n1. Angle.\n2. Temperature.\n3. Quit Converter.")

def angle_conversion_menuMsg():
    print("\n|=====>Input choices<=====|\n\nSelect a input choice\n\n1. Degree.\n2. Radians \n3. Gradians\n4. Quit Angle Converter.")

def temp_conv_menuMsg():
    print("\n|=====>Input choices<=====|\n\nSelect a input choice\n\n1. Celsius.\n2. Kelvin \n3. Farenheit\n4. Quit Temperature Converter.")

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
            # errmsg()
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
                    temp_conv_menuMsg()
                    input_choice = int(input("Enter input choice: "))
                    output_choice = int(input("Enter output choice: "))
                    key = (input_choice, output_choice)
                    print("Enter temperature: ", end='')
                    input_tmp = get_val()
                    if key in temp_conv_funcs:
                        from_tmp, to_tmp, tmp_func = temp_conv_funcs[key]
                        if input_tmp!=None:
                            print(f"{input_tmp} {from_tmp} = {tmp_func(input_tmp)} {to_tmp}")
                        else:
                            errmsg()
                case 3:
                    print("\nConverter menu closed\n")
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

def C_to_kelvin(tmp): return (tmp+273.15)
def C_to_Farenheit(tmp): return ((9/5)*tmp) + 32

def K_to_celsius(tmp): return (tmp-273.15)
def K_to_Farenheit(tmp): return C_to_Farenheit(K_to_celsius(tmp))

def F_to_celsius(tmp): return (5/9)*(tmp - 32)
def F_to_kelvin(tmp): return F_to_celsius(tmp) + 273.15


temp_conv_funcs = {
    (1,2): ("Celsius", "Kelvin", C_to_kelvin),
    (1,3): ("Celsius", "Farenheit", C_to_Farenheit),
    (2,1): ("Kelvin", "Celsius", K_to_celsius),
    (2,3): ("Kelvin", "Farenheit", K_to_Farenheit),
    (3,1): ("Farenheit", "Celsius", F_to_celsius),
    (3,2): ("Farenheit", "Kelvin", F_to_kelvin)
    }
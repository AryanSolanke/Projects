from std import *
from sci import *

def mode_choice_menu():
    print("\n======>Main Menu<======\n\n1. Standard\n2. Scientific\n3. Quit Calculator")

def std_calc_menuMsg():
    print("\n|=====>Operations<=====|\n\n1. Type expression\n2. Quit standard calculator\n\n|======================|")

def sci_calc_menuMsg():
    print("""\n|=========================>Operations<=========================|\n
          1. Basic trigo functions(sinx,cosx,tanx...)
          2. Inverse trigo functions(sin⁻¹x,cos⁻¹x,tan⁻¹x...)
          3. Hyperbolic trigo functions(sinhx, coshx, tanhx...)
          4. Inverse Hyperbolic trigo functions(sinh⁻¹x,cosh⁻¹x,tanh⁻¹x...)
          5. Quit scientific calculator.
          \n|===================================================================|""")

def std_calc_main_menu():
    while True:
        std_calc_menuMsg()
        try:
            op_num = int(input("Enter your choice: "))
            if not op_num:
                errmsg()
        except (ValueError, KeyboardInterrupt, UnboundLocalError):
            errmsg()
            continue
        match op_num:
            case 1:
                print(f"Result: {evaluate_expression()}")
            case 2:
                print("\nStandard calculator closed!")
                break
            case _:
                errmsg()

def sci_calc_main_menu():
    while True:
        sci_calc_menuMsg()
        try:
            op_num = int(input("Enter operation number: "))
            if not op_num:
                errmsg()
        except (ValueError, KeyboardInterrupt, UnboundLocalError):
            errmsg()
            continue
        match op_num:
            case 1:
                angle = get_angle()
                print(f"\nsin({angle}) = {sine(angle)}")
            case 2:
                angle = get_angle()
                print(f"\ncos({angle}) = {cosine(angle)}")
            case 3:
                angle = get_angle()
                print(f"\ntan({angle}) = {tangent(angle)}")
            case 4: 
                angle = get_angle()
                print(f"\ncot({angle}) = {cot(angle)}")
            case 5:
                angle = get_angle()
                print(f"\nsec({angle}) = {sec(angle)}")
            case 6:
                angle = get_angle()
                print(f"\ncosec({angle}) = {cosec(angle)}")
            case 7:
                print("\nScientific calculator closed!")
                break
            case _:
                errmsg()

if __name__ == '__main__':
    try:
        while True:
            mode_choice_menu()
            try:
                mode_choice = int(input("Select a mode for Calc: "))
            except ValueError:
                errmsg()
            match mode_choice:
                case 1:
                    std_calc_main_menu()
                case 2:
                    sci_calc_main_menu()
                case 3:
                    print("\nThank you for using Calculator!")
                    break
                case _:
                    errmsg()
    except(KeyboardInterrupt, EOFError):
            print("\nProgram interrupted by user. Thank you for using Calculator!")
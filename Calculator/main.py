from std import *
from sci import *
import textwrap

def mode_choice_menu():
    print("\n======>Main Menu<======\n\n1. Standard\n2. Scientific\n3. Quit Calculator")

def std_calc_menuMsg():
    print("\n|=====>Operations<=====|\n\n1. Type expression\n2. Quit standard calculator\n\n|======================|")

def sci_calc_menuMsg():
    print(textwrap.dedent("""
            |=========================>Operations<=========================|\n
            1. Basic trigo functions(sinx,cosx,tanx...)
            2. Inverse trigo functions(sin⁻¹x,cos⁻¹x,tan⁻¹x...)
            3. Hyperbolic trigo functions(sinhx, coshx, tanhx...)
            4. Inverse Hyperbolic trigo functions(sinh⁻¹x,cosh⁻¹x,tanh⁻¹x...)
            5. Quit scientific calculator.\n
            |==============================================================|\n"""))
    
def sci_calc_subMenu_msg(op_num):
    match op_num:
        case 1:
            print("\n|=====>Operations<=====|\n\n1. sinx\n2. cosx\n3. tanx\n4. cotx\n5. secx\n6. cosecx\n\n|======================|")
        case 2:
            print("\n|=====>Operations<=====|\n\n1. sin⁻¹x\n2. cos⁻¹x\n3. tan⁻¹x\n4. cot⁻¹x\n5. sec⁻¹x\n6. cosec⁻¹x\n\n|======================|")
        case 3:
            print("\n|=====>Operations<=====|\n\n1. sinhx\n2. coshx\n3. tanhx\n4. cothx\n5. sechx\n6. cosechx\n\n|======================|")
        case 4:
            print("\n|=====>Operations<=====|\n\n1. sinh⁻¹x\n2. cosh⁻¹x\n3. tanh⁻¹x\n4. coth⁻¹x\n5. sech⁻¹x\n6. cosech⁻¹x\n\n|======================|")
        case 5:
            print("\nScientific calculator Sub-menu exited...")
        case _:
            errmsg()


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
            op_num = int(input("Enter your choice: "))
            if not op_num:
                errmsg()
        except (ValueError, KeyboardInterrupt, UnboundLocalError):
            errmsg()
            continue
        match op_num:
            case 1:
                sci_calc_subMenu_msg(op_num)
                choice = int(input("Enter your choice: "))
                eval_trigo_func(op_num, choice)
            case 2:
                sci_calc_subMenu_msg(op_num)
                choice = int(input("Enter your choice: "))
                eval_trigo_func(op_num, choice)
            case 3:
                sci_calc_subMenu_msg(op_num)
                choice = int(input("Enter your choice: "))
                eval_trigo_func(op_num, choice)
            case 4: 
                sci_calc_subMenu_msg(op_num)
                choice = int(input("Enter your choice: "))
                eval_trigo_func(op_num, choice)
            case 5:
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
from std import *
from sci import *
import textwrap

def mode_choice_menu():
    print("\n======>Main Menu<======\n\n1. Standard\n2. Scientific\n3. Quit Calculator")

def std_calc_menuMsg():
    print("\n|=====>Operations<=====|\n\n1. Type expression\n2. Quit standard calculator\n\n|======================|")

def sci_calc_menuMsg():
    print(textwrap.dedent("""
                |============================>Operations<============================|\n
                1. Basic trigo functions
                    │──1.1 sin(x)
                    │──1.2 cos(x)
                    │──1.3 tan(x)
                    │──1.4 cot(x)
                    │──1.5 sec(x)
                    │──1.6 cosec(x)
                          
                2. Inverse trigo functions
                    │──2.1 sin⁻¹(x)
                    │──2.2 cos⁻¹(x)
                    │──2.3 tan⁻¹(x)
                    │──2.4 cot⁻¹(x)
                    │──2.5 sec⁻¹(x)
                    │──2.6 cosec⁻¹(x)
                          
                3. Hyperbolic trigo functions
                    │──3.1 sinh(x)
                    │──3.2 cosh(x)
                    │──3.3 tanh(x)
                    │──3.4 coth(x)
                    │──3.5 sech(x)
                    │──3.6 cosech(x)
                          
                4. Inverse Hyperbolic trigo functions
                    │──4.1 sinh⁻¹(x)
                    │──4.2 cosh⁻¹(x)
                    │──4.3 tanh⁻¹(x)
                    |_4.4 coth⁻¹(x)
                    |_4.5 sech⁻¹(x)
                    |_4.6 cosech⁻¹(x)
                          
                5. Show operations.
                6. Show history.
                7. Clear history.
                8. Quit scientific calculator.
                |====================================================================|\n"""))

def std_calc():
    while True:
        std_calc_menuMsg()
        try:
            op_num = int(input("Enter your choice: "))
            if not op_num:
                errmsg()
        except (ValueError, KeyboardInterrupt, UnboundLocalError,TypeError):
            errmsg()
            continue
        match op_num:
            case 1:
                exp = exp_input()
                print(f"Result: {evaluate_expression(exp)}")
            case 2:
                print("\nStandard calculator closed!")
                break
            case _:
                errmsg()

def sci_calc():
    while True:
        try:
            op_num = int(input("Enter operation number: "))
            match op_num:
                case 1|2|3|4:
                    pass
                case 5:
                    sci_calc_menuMsg()
                    continue
                case 6:
                    display_hist_sci_calc()
                    continue
                case 7:
                    clear_hist_sci_calc()
                    continue
                case 8:
                    print("\nScientific calculator closed!")
                    break
                case _:
                    errmsg()
                    break
            sub_op_num = int(input("Enter sub-opertion number: "))
            if validate_subOpNum(sub_op_num)==0: continue
            key = (op_num, sub_op_num)
            eval_trigo_func(key)
        except (ValueError, KeyboardInterrupt, UnboundLocalError, TypeError):
            errmsg()
            continue

if __name__ == '__main__':
    try:
        while True:
            mode_choice_menu()
            try:
                mode_choice = int(input("Select a mode for Calc: "))
            except (ValueError, TypeError):
                errmsg()
            match mode_choice:
                case 1:
                    std_calc()
                case 2:
                    sci_calc_menuMsg()
                    sci_calc()
                case 3:
                    print("\nThank you for using Calculator!")
                    break
                case _:
                    errmsg()
    except(KeyboardInterrupt, EOFError):
            print("\nProgram interrupted by user. Thank you for using Calculator!")
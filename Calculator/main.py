"""
Advanced Modular Calculator - Main Entry Point

Console-based calculator with standard arithmetic, scientific functions,
and unit conversions.
"""

import textwrap
from enum import IntEnum

from std import (
    errmsg,
    exp_input,
    evaluate_expression,
    display_hist_std_calc,
    clear_hist_std_calc
)
from sci import (
    display_hist_sci_calc,
    clear_hist_sci_calc,
    validate_subOpNum,
    eval_trigo_func
)
from converter import angle_converter


class MainMode(IntEnum):
    """Main calculator modes."""
    STANDARD = 1
    SCIENTIFIC = 2
    CONVERTER = 3
    QUIT = 4


class StdOperation(IntEnum):
    """Standard calculator operations."""
    EVALUATE = 1
    SHOW_HISTORY = 2
    CLEAR_HISTORY = 3
    QUIT = 4


class SciOperation(IntEnum):
    """Scientific calculator operations."""
    TRIG = 1
    INVERSE_TRIG = 2
    HYPERBOLIC = 3
    INVERSE_HYPERBOLIC = 4
    SHOW_MENU = 5
    SHOW_HISTORY = 6
    CLEAR_HISTORY = 7
    QUIT = 8


# ============================================================================
# Menu Display Functions
# ============================================================================

def mode_choice_menu() -> None:
    """Display main menu options."""
    print("\n|======>Main Menu<======|\n")
    print("1. Standard.\n2. Scientific.\n3. Converter\n4. Quit Calculator.")


def std_calc_menuMsg() -> None:
    print("\n|=====>Operations<=====|\n")
    print("\n|=====>Operations<=====|\n")
    print("1. Type expression.")
    print("2. Show history.")
    print("3. Clear history.")
    print("4. Quit standard calculator.")
    print("\n|======================|")


def sci_calc_menuMsg() -> None:
    """Display scientific calculator menu with all functions."""
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
                |====================================================================|
"""))


# ============================================================================
# Calculator Mode Functions
# ============================================================================

def std_calc() -> None:
    """
    Standard calculator interface.
    Handles expression evaluation and history management.
    """
    while True:
        std_calc_menuMsg()
        try:
            op_num = int(input("Enter your choice: "))

            if op_num == StdOperation.EVALUATE:
                exp = exp_input()
                print(f"Result: {evaluate_expression(exp)}")

            elif op_num == StdOperation.SHOW_HISTORY:
                display_hist_std_calc()

            elif op_num == StdOperation.CLEAR_HISTORY:
                clear_hist_std_calc()

            elif op_num == StdOperation.QUIT:
                print("\nStandard calculator closed!")
                break
            else:
                errmsg()

        except (ValueError, KeyboardInterrupt, UnboundLocalError, TypeError):
            errmsg()
            continue


def sci_calc() -> None:
    """
    Scientific calculator interface.
    Handles trignometric and hyperbolic function calculations.
    """
    while True:
        try:
            op_num = int(input("Enter operation number: "))

            if op_num in (SciOperation.TRIG, SciOperation.INVERSE_TRIG,
                          SciOperation.HYPERBOLIC, SciOperation.INVERSE_HYPERBOLIC):
                # Get sub-oeration for function categories 1-4
                sub_op_num = int(input("Enter sub-operation number: "))

                if validate_subOpNum(sub_op_num) == 0:
                    continue

                key = (op_num, sub_op_num)
                eval_trigo_func(key)

            elif op_num == SciOperation.SHOW_MENU:
                sci_calc_menuMsg()

            elif op_num == SciOperation.SHOW_HISTORY:
                display_hist_sci_calc()
            
            elif op_num == SciOperation.CLEAR_HISTORY:
                clear_hist_sci_calc()
            
            elif op_num == SciOperation.QUIT:
                print("\nScientific calculator closed!")
                break
            else:
                errmsg()
            
        except (ValueError, KeyboardInterrupt, UnboundLocalError, TypeError):
            errmsg()
            continue


# ============================================================================
# Main Entry Point
# ============================================================================

def main() -> None:
    """Main application loop."""
    try:
        while True:
            mode_choice_menu()
            try:
                mode_choice = int(input("Select a mode for Calc: "))
            except (ValueError, TypeError):
                errmsg()
                continue

            if mode_choice == MainMode.STANDARD:
                std_calc()
            
            elif mode_choice == MainMode.SCIENTIFIC:
                sci_calc_menuMsg()
                sci_calc()
            
            elif mode_choice == MainMode.CONVERTER:
                angle_converter()
            
            elif mode_choice == MainMode.QUIT:
                print("\nThank you for using Calculator!\n")
                break
            else:
                errmsg()

    except(KeyboardInterrupt, EOFError):
            print("\nProgram interrupted by user. Thank you for using Calculator!")


if __name__ == '__main__':
    main()

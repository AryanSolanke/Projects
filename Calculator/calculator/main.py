"""
Advanced Modular Calculator - Main Entry Point

Console-based calculator with standard arithmetic, scientific functions,
unit conversions, and a full programmer calculator.
"""

from enum import IntEnum

from calculator.standard import (
    errmsg,
    std_calc
)
from calculator.scientific import (
    display_hist_sci_calc,
    clear_hist_sci_calc,
    validate_subOpNum,
    eval_trigo_func,
    sci_calc_menuMsg,
)
from calculator.router import converter_menu
from calculator.programmer import programmer_calc


class MainMode(IntEnum):
    """Main calculator modes."""
    STANDARD   = 1
    SCIENTIFIC = 2
    CONVERTER  = 3
    PROGRAMMER = 4
    QUIT       = 5


class SciOperation(IntEnum):
    """Scientific calculator operations."""
    TRIG               = 1
    INVERSE_TRIG       = 2
    HYPERBOLIC         = 3
    INVERSE_HYPERBOLIC = 4
    SHOW_MENU          = 5
    SHOW_HISTORY       = 6
    CLEAR_HISTORY      = 7
    QUIT               = 8


# ============================================================================
# Menu Display Functions
# ============================================================================

def mode_choice_menu() -> None:
    """Display main menu options."""
    print("\n" + "="*50)
    print("ADVANCED MODULAR CALCULATOR")
    print("="*50)
    print("1. Standard Calculator")
    print("2. Scientific Calculator")
    print("3. Unit Converter")
    print("4. Programmer Calculator")
    print("5. Quit Calculator")
    print("="*50)


# ============================================================================
# Calculator Mode Functions
# ============================================================================




def sci_calc() -> None:
    """
    Scientific calculator interface.
    Handles trigonometric and hyperbolic function calculations.
    """
    while True:
        try:
            op_num = int(input("\nEnter operation number: "))

            if op_num in (SciOperation.TRIG, SciOperation.INVERSE_TRIG,
                          SciOperation.HYPERBOLIC, SciOperation.INVERSE_HYPERBOLIC):
                # Get sub-operation for function categories 1-4
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
                print("\n Scientific calculator closed!\n")
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
    print("\n" + "="*50)
    print("   Welcome to Advanced Modular Calculator!")
    print("="*50)
    
    try:
        while True:
            mode_choice_menu()
            try:
                mode_choice = int(input("\nSelect a mode: "))
            except (ValueError, TypeError):
                errmsg()
                continue

            if mode_choice == MainMode.STANDARD:
                std_calc()

            elif mode_choice == MainMode.SCIENTIFIC:
                sci_calc_menuMsg()
                sci_calc()

            elif mode_choice == MainMode.CONVERTER:
                converter_menu()

            elif mode_choice == MainMode.PROGRAMMER:
                programmer_calc()

            elif mode_choice == MainMode.QUIT:
                print("\n" + "="*50)
                print("   Thank you for using Calculator!")
                print("="*50 + "\n")
                break
            else:
                errmsg()

    except (KeyboardInterrupt, EOFError):
        print("\nProgram interrupted by user. Thank you for using Calculator!")


if __name__ == '__main__':
    main()

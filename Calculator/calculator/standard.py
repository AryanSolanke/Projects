"""
Standard Calculator Module

Provides expression evaluation with history tracking and error handling.
"""

from calculator.exceptions import UnbalancedParenthesesError, ExpressionError, CalculatorError, NullInputError
from enum import IntEnum
from decimal import Decimal, InvalidOperation, localcontext
import re

from calculator.config import DECIMAL_PRECISION, DISPLAY_PRECISION, STD_HISTORY_FILE

# ============================================================================
# Constants
# ============================================================================

HISTORY_FILE = STD_HISTORY_FILE
FLOAT_LIKE_MAX_EXP = 308

_NUMBER_PATTERN = re.compile(r"(?:\d+\.\d+|\d+|(?<![\d.])\.\d+)")


def errmsg() -> None:
    """Display standard error message for invalid input."""
    print("Error: Invalid input.")


class StdOperation(IntEnum):
    """Standard calculator operations."""
    EVALUATE      = 1
    SHOW_HISTORY  = 2
    CLEAR_HISTORY = 3
    QUIT          = 4

# ============================================================================
# Result Formatting
# ============================================================================

def format_answer(result: Decimal) -> str:
    """
    Format numerical result removing trailing zeros and artifacts.
    
    Args:
        result: Numerical result to format

    Returns:
        Formatted string representation
    """
    if not isinstance(result, Decimal):
        result = Decimal(str(result))
    formatted_res = f"{result:.{DISPLAY_PRECISION}g}"
    stripped_res = formatted_res.rstrip("0").rstrip(".")
    # Normalize negative zero
    return "0" if stripped_res == "-0" else stripped_res


# ============================================================================
# Menu Display Functions
# ============================================================================

def std_calc_menuMsg() -> None:
    """Display standard calculator menu options."""
    print("\n" + "="*40)
    print("STANDARD CALCULATOR")
    print("="*40)
    print("1. Type expression")
    print("2. Show history")
    print("3. Clear history")
    print("4. Quit standard calculator")
    print("="*40)


# ============================================================================
# File Handling Functions
# ============================================================================

def record_history_std_calc(exp: str, result: str) -> None:
    """
    Append calculation to history file.
    
    Args:
        exp: Expression that was evaluated
        result: Computed result
    """
    try:
        with HISTORY_FILE.open('a', encoding="utf-8") as f:
            f.write(f"{exp} = {result}\n")
    except (FileNotFoundError, PermissionError, UnicodeDecodeError, OSError):
        print("Internal Error: Failed to record history")


def display_hist_std_calc() -> None:
    """Display calculation history from file."""
    try:
        if not HISTORY_FILE.exists():
            print("No history available.")
            return
        
        history = HISTORY_FILE.read_text(encoding="utf-8").splitlines()
        if not history:
            print("History is empty.")
            return
            
        print("\n" + "="*40)
        print("CALCULATION HISTORY")
        print("="*40)
        for line in history:
            print(f"  {line}")
        print("="*40 + "\n")
    except (PermissionError, UnicodeDecodeError, OSError):
        print("Internal Error: Failed reading history")


def clear_hist_std_calc() -> None:
    """Clear all calculation history from file."""
    try:
        HISTORY_FILE.write_text("", encoding="utf-8")
        print("   History cleared successfully!")
    except (FileNotFoundError, PermissionError, UnicodeDecodeError, OSError):
        print("Internal Error: Failed to clear history")


# ============================================================================
# Expression Input and Validation
# ============================================================================

def exp_input() -> str:
    """
    Prompt user for expression input.
    
    Returns:
        Expression string entered by user
    """
    exp = input("Enter expression (e.g., 2+3*4): ")
    return exp


def validate_exp(exp: str) -> bool:
    """
    Validate arithmetic expression for correctness.
    
    Args:
        exp: Expression to validate

    Returns:
        True if valid, False otherwise
    """
    # Check for empty input
    if not exp.strip():
        raise NullInputError()
    
    # Check for unbalanced parentheses
    if exp.count('(') != exp.count(')'):
        raise UnbalancedParenthesesError()
    
    # Check for allowed characters
    allowed_chars = "0123456789+-*/%(). "
    for char in exp:
        if char not in allowed_chars:
            print("Error: Invalid Expression. Please enter a valid character [0123456789+-*/%(). ]")
            return False

    return True


# ============================================================================
# Expression Evaluation
# ============================================================================

def evaluate_expression(exp: str) -> str:
    """
    Evaluate arithmetic expression and return formatted result.
    
    Args:
        exp: Arithmetic expression to evaluate

    Returns:
        Formatted result string, or "0" if evaluation fails
    """
    try:
        if not validate_exp(exp):
            return "0"
    
        decimal_exp = _NUMBER_PATTERN.sub(
            lambda m: f"Decimal('{m.group(0)}')", exp
        )
        with localcontext() as ctx:
            ctx.prec = max(DECIMAL_PRECISION, 28)
            result = eval(decimal_exp, {"Decimal": Decimal})

        if not isinstance(result, Decimal):
            result = Decimal(str(result))

        if not result.is_finite():
            raise InvalidOperation("Math error: result is not finite")
        
        if result.is_finite() and result.adjusted() > FLOAT_LIKE_MAX_EXP:
            raise OverflowError("Math error: Result overflowed.")
        
        formatted_result = format_answer(result)
        record_history_std_calc(exp, formatted_result)
        return formatted_result 
    except ZeroDivisionError:
        raise InvalidOperation("Math error: Cannot divide by zero.")
    
    except InvalidOperation:
        raise ExpressionError("Math error: Invalid mathematical operation")
    
    except TypeError:
        raise ExpressionError()

    except OverflowError:
        raise OverflowError("Math error: Result overflowed.")
    
# ============================================================================
# Main Interface Function
# ============================================================================

def std_calc() -> None:
    """
    Standard calculator interface.
    Handles expression evaluation and history management.
    """
    while True:
        std_calc_menuMsg()
        try:
            op_num = int(input("\nEnter your choice: "))

            if op_num == StdOperation.EVALUATE:
                exp = exp_input()
                result = evaluate_expression(exp)
                print(f" Result: {result}")

            elif op_num == StdOperation.SHOW_HISTORY:
                display_hist_std_calc()

            elif op_num == StdOperation.CLEAR_HISTORY:
                clear_hist_std_calc()

            elif op_num == StdOperation.QUIT:
                print("\n Standard calculator closed!\n")
                break
            else:
                print("Invalid input: Please select 1-4")

        except CalculatorError as e:
            print(e)
            continue
        except OverflowError as e:
            print(e)
            continue
        except ValueError:
            print("Invalid input: Please select 1-4")
            continue
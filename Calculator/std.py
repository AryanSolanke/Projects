"""
Standard Calculator Module

Provides expression evaluation with history tracking and error handling.
"""

from decimal import Decimal, InvalidOperation, DivisionByZero, localcontext
from pathlib import Path
import re

# ============================================================================
# Constants
# ============================================================================

HISTORY_FILE = Path("std_calc_history_file.txt")
DECIMAL_PRECISION = 14
FLOAT_LIKE_MAX_EXP = 308

_NUMBER_PATTERN = re.compile(r"(?:\d+\.\d+|\d+|(?<![\d.])\.\d+)")


# ============================================================================
# Error Handling
# ============================================================================

def errmsg() -> None:
    """Display standard error message for invalid input."""
    print("Error: Invalid input.")


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
    formatted_res = f"{result:.{DECIMAL_PRECISION}f}"
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
    except FileNotFoundError:
        print("Failed to record history")
    except Exception:
        errmsg()


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
    except Exception:
        errmsg()


def clear_hist_std_calc() -> None:
    """Clear all calculation history from file."""
    try:
        HISTORY_FILE.write_text("", encoding="utf-8")
        print("   History cleared successfully!")
    except FileNotFoundError:
        print("Failed to clear history")
    except Exception:
        errmsg()


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
        print("No input given")
        return False
    
    # Check for unbalanced parentheses
    if exp.count('(') != exp.count(')'):
        print("Error: Unbalanced parentheses")
        return False
    
    # Check for allowed characters
    allowed_chars = "0123456789+-*/%(). "
    for char in exp:
        if char not in allowed_chars:
            print(f"Error: Character '{char}' not allowed")
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
    if not validate_exp(exp):
        return "0"
    
    try:
        decimal_exp = _NUMBER_PATTERN.sub(
            lambda m: f"Decimal('{m.group(0)}')", exp
        )
        with localcontext() as ctx:
            ctx.prec = max(DECIMAL_PRECISION, 28)
            result = eval(decimal_exp, {"Decimal": Decimal})
        if not isinstance(result, Decimal):
            result = Decimal(str(result))
        if not result.is_finite():
            raise InvalidOperation
        if result.is_finite() and result.adjusted() > FLOAT_LIKE_MAX_EXP:
            raise OverflowError
        formatted_result = format_answer(result)
        record_history_std_calc(exp, formatted_result)
        return formatted_result
    except (SyntaxError, ZeroDivisionError, TypeError, OverflowError, InvalidOperation, DivisionByZero):
        errmsg()
        return "0"

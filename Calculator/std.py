"""
Standard Calculator Module

Provides expression evaluation with history tracking and error handling.
"""

from pathlib import Path
from typing import Optional

#Constants
HISTORY_FILE = Path("std_calc_history_file.txt")
DECIMAL_PRECISION = 14

def errmsg() -> None:
    """Display standard error message."""
    print("Error: Invalid input.")


def format_answer(result: float) -> str:
    """
    Format numerical result removing trailing zeros and artifacts.
    
    Args:
        Result: Numerical result to format

    Returns:
        Formatted string representation
    """
    formatted_res = f"{result:.{DECIMAL_PRECISION}f}"
    stripped_res = formatted_res.rstrip("0").rstrip(".")
    # Normalize negative zero
    return "0" if stripped_res == "-0" else stripped_res


def record_history_std_calc(exp: str, result: str) -> None:
    """
    Append calculation to history file.
    
    Args:
        exp: Expression to be evaluated
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
            print("Failed to display history.")
            return
        
        history =  HISTORY_FILE.read_text(encoding="utf-8").splitlines()
        print("History:")
        for line in history:
            print(line)
    except Exception:
        errmsg()


def clear_hist_std_calc() -> None:
    """Clear history from file."""
    try:
        HISTORY_FILE.write_text("", encoding="utf-8")
        print("History cleared successfully!")
    except FileNotFoundError:
        print("Failed to clear history")
    except Exception:
        errmsg()

def exp_input() -> str:
    """
    Prompt user for expression input.
    
    Returns: 
        Expression string entered by user
    """
    exp = input("Enter expression(eg. 2+3*4): ")
    return exp

def validate_exp(exp: str) -> bool:
    """
    Docstring for validate_exp.
    
    Args:
        exp: Expression to be validated

    Returns: 
        True if valid, False otherwise
    """
    # Check for unbalanced parenthesis
    if exp.count('(') != exp.count(')'):
        print("Error: Unbalanced paranthesis")
        return False
    
    # Check for empty input
    if not exp.strip():
        print("No input given")
        return False
    
    # Check for allowed characters
    allowed_chars = "0123456789+-*/%(). "
    for char in exp:
        if char not in allowed_chars:
            print("Error: characters not allowed")
            return False
        
    return True


def evaluate_expression(exp: str) -> str:
    """
    Docstring for evaluate_expression
    
    Args:
        exp: Arithmetic expression to evaluate

    Returns:
        Formatted result string, or "0" if evaluation fails
    """
    if not validate_exp(exp):
        return "0"
    
    try:
        result = float(f"{eval(exp)}")
        formatted_result = format_answer(result)
        record_history_std_calc(exp, formatted_result)
        return formatted_result
    except (SyntaxError, ZeroDivisionError, TypeError, OverflowError):
        errmsg()
        return "0"
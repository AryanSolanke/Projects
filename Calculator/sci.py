"""
Scientific Calculator Module

Provides trignometric, hyperbolic, and inverse functions with strict domain validation.
Supports history tracking and precise numerical formatting.
"""

from math import (
    sin, cos, tan, sinh, cosh, tanh, 
    asin, acos, atan, asinh, acosh, atanh, 
    radians, degrees, log, isclose
)
from pathlib import Path
from typing import Callable, Tuple, Optional, Union
from dataclasses import dataclass
from enum import IntEnum

# Import error message utility from std module
from std import errmsg


# ============================================================================
# Constants and Configuration
# ============================================================================

HISTORY_FILE = Path("sci_calc_history_file.txt")
RESULT_PRECISION = 9 # Significant figures for output formatting
ANGLE_TOLERANCE = 1e-9 # Tolerance for asymptote detection

class FunctionCategory(IntEnum):
    """Enumeration of function categories for cleaner switch logic."""
    TRIGNOMETRIC = 1
    HYPERBOLIC = 2
    INVERSE_TRIGNOMETRIC = 3
    INVERSE_HYPERBOLIC = 4


class SubOperation(IntEnum):
    """Enumeration of sub-operations within each categpry."""
    FUNC_1 = 1  # sin/sinh/sin⁻¹/sinh⁻¹
    FUNC_2 = 2  # cos/cosh/cos⁻¹/cosh⁻¹
    FUNC_3 = 3  # tan/tanh/tan⁻¹/tanh⁻¹
    FUNC_4 = 4  # cot/coth/cot⁻¹/coth⁻¹
    FUNC_5 = 5  # sec/sech/sec⁻¹/sech⁻¹
    FUNC_6 = 6  # cosec/cosech/cosec⁻¹/cosech⁻¹


# ============================================================================
# Custom Exceptions
# ============================================================================

class DomainError(ValueError):
    """Raised when input is outside the valid domain for a function."""
    pass


class AsymptoteError(ValueError):
    """Raised when input approaches a function's asymptote."""
    pass


# ============================================================================
# Input/Output Utilities
# ============================================================================

def get_val() -> Optional[float]:
    """Prompt user for numeric input with error handling.
    
    Returns:
        float if valid, None otherwise
    """
    try:
        val = float(input())
        return val
    except (ValueError, SyntaxError, TypeError):
        errmsg()
        return None
    

def format_result(result: float) -> str:
    """Format numerical result with intelligent precision.

    Removes trailing zeros and floating-point artifacts.
    Normalizes -0.0 to 0
    
    Args:
        result: Numerical result to be format
    
    Returns:
        String representation with appropriate precision
        """
    return f"{result:.{RESULT_PRECISION}g}"


# ============================================================================
# History Management
# ============================================================================

def display_hist_sci_calc() -> None:
    """Display calculation history from file."""
    try:
        if not HISTORY_FILE.exists():
            print("\nNo history file found. Perform a calculation first!")

        history = HISTORY_FILE.read_text(encoding="utf-8").strip()

        if not history:
            print("\nHistory is currently empty.")
        else:
            print("\n--- Scientific Calculation History ---")
            print(history)

    except Exception as e:
        print(f"Error reading history: {e}")


def record_history_sci_calc(name: str, val: float, answer: str) -> None:
    """
    Append calculation to history file.
    
    Args:
        name: Function name
        val: Input val
        answer: Computed result
    """
    try:
        with HISTORY_FILE.open(encoding="utf-8") as f:
            f.write(f"{name}({val}) = {answer}\n")
    except Exception as e:
        print(f"File Error: Could not record history. ({e})")

def clear_hist_sci_calc() -> None:
    """Clear all history by truncating the history file."""
    try:
        with HISTORY_FILE.open("", encoding="utf-8"):
            print("Scientific history cleared successfully!")
    except Exception as e:
        print(f"Could not clear history: {e}")


# ============================================================================
# Input Validation
# ============================================================================

def validate_subOpNum(sub_op_num: int) -> int:
        """
        Validate sub-operation number.
        
        Args:
            sub_op_num: Operation number (1-6)
        
        Returns:
            1 if valid, 0 otherwise
        """
        if 1 <= sub_op_num <= 6:
                return 1
        errmsg()
        return 0
            

# ============================================================================
# Domain Validators
# ============================================================================

def _validate_trig_asymptote(sub_op_num: int, angle: float) -> None:
    """
    Check for asymptotes in regular trignometric functions.
    
    Args:
        sub_op_num: Specific trig function indentifier
        angle: Angle in degrees
    
    Raises:
        AsymptoteError: If angle is at an asymptote
    """
    #cot(x) and cosec(x) undefined where sin(x) = 0 (at n*180°)
    if sub_op_num in (SubOperation.FUNC_4, SubOperation.FUNC_6):
        if isclose(angle % 180, 0, abs_tol=ANGLE_TOLERANCE):
            raise AsymptoteError("Error: Division by zero (Asymptote at n*180°)")
    
    # Undefined where cos(x) = 0: tan(x), sec(x)
        if sub_op_num in (SubOperation.FUNC_3, SubOperation.FUNC_5):
            if isclose(angle % 180, 90, abs_tol=ANGLE_TOLERANCE):
                raise AsymptoteError("Error: Division by zero (Asymptote at n*180° + 90°)")


def _validate_hyperbolic_asymptote(sub_op_num: int, val: float) -> None:
    """
    Check for asymptotes in hyperbolic functions.
    
    Args:
        sub_op_num: Specific trig function indentifier
        val: Input val

    Raises:
        AsymptoteError:  If value is at an asymptote
    """
    # coth(0) and cosech(0) are undefined
    if sub_op_num in (SubOperation.FUNC_4, SubOperation.FUNC_6) and val == 0:
        raise AsymptoteError("Error: Division by zero (Undefined at x=0)")


def _validate_inverse_trig_domain(sub_op_num: int, val: float) -> None:
    """
    Validate domain for inverse trignometric functions.

    Args:
        sub_op_num: Specific trig function indentifier
        val: Input val

    Raises:
        DomainError: If value is outside valid domain
    """
    # arcsin and arccos require |x| <= 1
    if sub_op_num in (SubOperation.FUNC_1, SubOperation.FUNC_2):
        if val < -1 or val > 1:
            raise DomainError("Domain Error: Input x must satisfy |x| <= 1")
    
    # arcsec and arccosec require |x| >= 1
    if sub_op_num in (SubOperation.FUNC_5, SubOperation.FUNC_6):
        if -1 < val < 1:
            raise DomainError("Domain Error: Input x must satisfy |x| >= 1")


def _validate_inverse_hyperbolic_domain(sub_op_num: int, val: float) -> None:
    """
    Validate domain for inverse hyperbolic functions.

    Args:
        sub_op_num: Specific trig function indentifier
        val: Input val

    Raises:
        DomainError: If value is outside valid domain
    """
    domain_checks = {
        SubOperation.FUNC_2:(
            lambda x: x < 1,
            "Domain Error: acosh(x) requires x >= 1"      
        ),
        SubOperation.FUNC_3: (
            lambda x: x <= -1 or x >= 1,
            "Domain Error: atanh(x) requires x in open interval (-1, 1)"
        ),
        SubOperation.FUNC_4: (
            lambda x:-1 <= x <= 1,
            "Domain Error: acoth(x) requires x outside closed interval [-1, 1]"
        ),
        SubOperation.FUNC_5:(
            lambda x: x <= 0 or x > 1,
            "Domain Error: asech(x) requires x in range (0, 1]"
        ),
        SubOperation.FUNC_6:(
            lambda x: x == 0,
            "Domain Error: acosech(x) is undefined at x=0"
        ),
    }

    if sub_op_num in domain_checks:
        check_func, error_msg = domain_checks[sub_op_num]
        if check_func(val):
            raise DomainError(error_msg)


# ============================================================================
# Core Mathematical Functions
# ============================================================================

# Standard Trignometric Functions (input in degrees)
def sine(angle: float) -> float: 
    """Calculate sine of angle in degrees."""
    return sin(radians(angle))


def cosine(angle: float) -> float: 
    """Calculate cosine of angle in degrees."""
    return cos(radians(angle))


def tangent(angle: float) -> float: 
    """Calculate tangent of angle in degrees."""
    return tan(radians(angle))


def cot(angle: float) -> float: 
    """Calculate cotangent of angle in degrees."""
    return cos(radians(angle))/sin(radians(angle))


def sec(angle: float) -> float: 
    """Calculate secant of angle in degrees."""
    return 1/cos(radians(angle))


def cosec(angle: float) -> float: 
    """Calculate cosecant of angle in degrees."""
    return 1/sin(radians(angle))



# Inverse Trignometric Functions (output in degrees)
def sine_inv(val: float) -> float: 
    """Calculate arcsine, returns result in degrees."""
    return degrees(asin(val))


def cosine_inv(val: float) -> float: 
    """Calculate arccosine, returns result in degrees."""
    return degrees(acos(val))


def tangent_inv(val: float) -> float: 
    """Calculate arctangent, returns result in degrees."""
    return degrees(atan(val))


def cot_inv(val: float) -> float: 
    """Calculate arccotangent, returns result in degrees."""
    return degrees(atan(1/val))


def sec_inv(val: float) -> float: 
    """Calculate arcsecant, returns result in degrees."""
    return degrees(acos(1/val))


def cosec_inv(val: float) -> float: 
    """Calculate arccosecant, returns result in degrees."""
    return degrees(asin(1/val))


# Hyperbolic Functions
def sineh(val: float) -> float:
    """Calculate hyperbolic sine."""
    return sinh(val)


def cosineh(val: float) -> float:
    """Calculate hyperbolic cosine."""
    return cosh(val)


def tangenth(val: float) -> float:
    """Calculate hyperbolic tangent."""
    return tanh(val)


def coth(val: float) -> float:
    """Calculate hyperbolic cotangent."""
    return cosh(val)/sineh(val)


def sech(val: float) -> float:
    """Calculate hyperbolic secant."""
    return 1/cosh(val)


def cosech(val: float) -> float:
    """Calculate hyperbolic cosecant."""
    return 1/sinh(val)


# Inverse Hyperbolic Functions
def sineh_inv(val: float) -> float:
    """Calculate inverse hyperbolic sine."""
    return asinh(val)


def cosineh_inv(val: float) -> float:
    """Calculate inverse hyperbolic cosine."""
    return acosh(val)


def tangenth_inv(val: float) -> float:
    """Calculate inverse hyperbolic tangent."""
    return atanh(val)


def coth_inv(val: float) -> float:
    """Calculate inverse hyperbolic cotangent."""
    return 0.5 * log((val + 1) / (val - 1))


def sech_inv(val: float) -> float:
    """Calculate inverse hyperbolic secant."""
    return acosh(1 / val)


def cosech_inv(val: float) -> float:
    """Calculate inverse hyperbolic cosecant."""
    return asinh(1 / val)


# ============================================================================
# Function Registry
# ============================================================================

#Dictionary mapping (category, sub_op) tuples to (name, function) pairs
trigo_funcs: dict[Tuple[int, int], Tuple[str, Callable[[float], float]]]= {
    # Standard Trignometric
    (FunctionCategory.TRIGNOMETRIC, SubOperation.FUNC_1): ("sin", sine),
    (FunctionCategory.TRIGNOMETRIC, SubOperation.FUNC_2): ("cos", cosine),
    (FunctionCategory.TRIGNOMETRIC, SubOperation.FUNC_3): ("tan", tangent),
    (FunctionCategory.TRIGNOMETRIC, SubOperation.FUNC_4): ("cot", cot),
    (FunctionCategory.TRIGNOMETRIC, SubOperation.FUNC_5): ("sec", sec),
    (FunctionCategory.TRIGNOMETRIC, SubOperation.FUNC_6): ("cosec", cosec),

    # Hyperbolic
    (FunctionCategory.HYPERBOLIC, SubOperation.FUNC_1): ("sinh", sineh),
    (FunctionCategory.HYPERBOLIC, SubOperation.FUNC_2): ("cosh", cosineh),
    (FunctionCategory.HYPERBOLIC, SubOperation.FUNC_3): ("tanh", tangenth),
    (FunctionCategory.HYPERBOLIC, SubOperation.FUNC_4): ("coth", coth),
    (FunctionCategory.HYPERBOLIC, SubOperation.FUNC_5): ("sech", sech),
    (FunctionCategory.HYPERBOLIC, SubOperation.FUNC_6): ("cosech", cosech),

    # Inverse Trignometric
    (FunctionCategory.INVERSE_TRIGNOMETRIC, SubOperation.FUNC_1): ("sin⁻¹", sine_inv),
    (FunctionCategory.INVERSE_TRIGNOMETRIC, SubOperation.FUNC_2): ("cos⁻¹", cosine_inv),
    (FunctionCategory.INVERSE_TRIGNOMETRIC, SubOperation.FUNC_3): ("tan⁻¹", tangent_inv),
    (FunctionCategory.INVERSE_TRIGNOMETRIC, SubOperation.FUNC_4): ("cot⁻¹", cot_inv),
    (FunctionCategory.INVERSE_TRIGNOMETRIC, SubOperation.FUNC_5): ("sec⁻¹", sec_inv),
    (FunctionCategory.INVERSE_TRIGNOMETRIC, SubOperation.FUNC_6): ("cosec⁻¹", cosec_inv),

    # Inverse Hyperbolic
    (FunctionCategory.INVERSE_HYPERBOLIC, SubOperation.FUNC_1): ("sinh⁻¹", sineh_inv),
    (FunctionCategory.INVERSE_HYPERBOLIC, SubOperation.FUNC_2): ("cosh⁻¹", cosineh_inv),
    (FunctionCategory.INVERSE_HYPERBOLIC, SubOperation.FUNC_3): ("tanh⁻¹", tangenth_inv),
    (FunctionCategory.INVERSE_HYPERBOLIC, SubOperation.FUNC_4): ("coth⁻¹", coth_inv),
    (FunctionCategory.INVERSE_HYPERBOLIC, SubOperation.FUNC_5): ("sech⁻¹", sech_inv),
    (FunctionCategory.INVERSE_HYPERBOLIC, SubOperation.FUNC_6): ("cosech⁻¹", cosech_inv)
}


# ============================================================================
# Main Calculation Logic
# ============================================================================

def validate_and_eval(
        op_num: int,
        sub_op_num: int,
        name: str,
        func: Callable[[float], float],
        val: float
) -> str:
    """
    Validate input domain and execute scientific calculation.
    
    This function performs domain validation before computation  to ensure
    mathematical correctness and provide meaningful error messages.
    
    Args:
        op_num: Category of function (Trignometric, Hyperbolic, etc.)
        sub_op_num: Specific function identifier within category
        name: Display name of the function
        func: The mathematical function to execute
        val: The input value/angle
    
    Returns:
        Formatted result string or descriptive error message
    """
    try:
        # Perform domain validation based on function category
        if op_num == FunctionCategory.TRIGNOMETRIC:
            _validate_trig_asymptote(sub_op_num, val)

        elif op_num == FunctionCategory.HYPERBOLIC:
            _validate_hyperbolic_asymptote(sub_op_num, val)
        
        elif op_num == FunctionCategory.INVERSE_TRIGNOMETRIC:
            _validate_inverse_trig_domain(sub_op_num, val)
            if sub_op_num == SubOperation.FUNC_4 and val == 0:
                return f"{name}({val}) = 90"

        elif op_num == FunctionCategory.INVERSE_HYPERBOLIC:
            _validate_inverse_hyperbolic_domain(sub_op_num, val)

        # Execute calculation and format result
        result = func(val)
        formatted_result = format_result(result)
        record_history_sci_calc(name, val, formatted_result)
        return f"{name}({val}) = {formatted_result}"
    
    except (DomainError, AsymptoteError) as e:
        # Return domain/Asymptote errors as strings for backward compatibility
        return str(e)
    
    except (ValueError, ArithmeticError):
        return f"Math Error: {e}"
    
    except Exception as e:
        # Catch unexpected runtime exceptions
        return f"System Error: {type(e).__name__}"


def eval_trigo_func(key: Tuple[int, int]) -> None:
    """
    Evaluate trignometric function based on user input.
    
    Args:
        key: Tuple of (category, sub_operation) identifying the function
    """
    if key not in trigo_funcs:
        errmsg()
        return None
    
    op_num, sub_op_num = key
    name, func = trigo_funcs[key]

    print("Enter angle:" if op_num == FunctionCategory.TRIGNOMETRIC else "Enter value: ", end='')
    val = get_val()
    if val is not None:
        answer = validate_and_eval(op_num, sub_op_num, name, func, val)
        print(answer)

def print_eval(name, val, func):
    result = format_result(func(val))
    record_history_sci_calc(name, val, result)
    return f"{name}({val}) = {result}"

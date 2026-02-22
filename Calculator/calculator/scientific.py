"""
Scientific Calculator Module

Provides trigonometric, hyperbolic, and inverse functions with strict domain validation.
Supports history tracking and precise numerical formatting.
"""

from decimal import Decimal, InvalidOperation, localcontext
from typing import Callable, Tuple, Optional
from enum import IntEnum
from textwrap import dedent
from calculator.exceptions import CalculatorError, ExpressionError, InvalidInputError, AsymptoteError, DomainError
from calculator.config import SCI_HISTORY_FILE, DISPLAY_PRECISION, INTERNAL_PRECISION


# ============================================================================
# Menu Display Function(s)
# ============================================================================

def sci_calc_menuMsg() -> None:
    """Display scientific calculator menu with all functions."""
    print(dedent("""
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
                    │──4.4 coth⁻¹(x)
                    │──4.5 sech⁻¹(x)
                    │──4.6 cosech⁻¹(x)
                          
                5. Show operations.
                6. Show history.
                7. Clear history.
                8. Quit scientific calculator.
                |====================================================================|
"""))


# ============================================================================
# Constants and Configuration
# ============================================================================

HISTORY_FILE = SCI_HISTORY_FILE
RESULT_PRECISION = DISPLAY_PRECISION  # Significant figures for output formatting
ANGLE_TOLERANCE = Decimal("1e-9")  # Tolerance for asymptote detection

class FunctionCategory(IntEnum):
    """Enumeration of function categories for cleaner switch logic."""
    TRIGONOMETRIC = 1
    HYPERBOLIC = 2
    INVERSE_TRIGONOMETRIC = 3
    INVERSE_HYPERBOLIC = 4


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


class SubOperation(IntEnum):
    """Enumeration of sub-operations within each categpry."""
    FUNC_1 = 1  # sin/sinh/sin⁻¹/sinh⁻¹
    FUNC_2 = 2  # cos/cosh/cos⁻¹/cosh⁻¹
    FUNC_3 = 3  # tan/tanh/tan⁻¹/tanh⁻¹
    FUNC_4 = 4  # cot/coth/cot⁻¹/coth⁻¹
    FUNC_5 = 5  # sec/sech/sec⁻¹/sech⁻¹
    FUNC_6 = 6  # cosec/cosech/cosec⁻¹/cosech⁻¹


# ============================================================================
# Input/Output Utilities
# ============================================================================

def _to_decimal(value: Decimal | int | str) -> Decimal:
    if isinstance(value, Decimal):
        return value
    if isinstance(value, int):
        return Decimal(value)
    try:
        return Decimal(str(value))
    except InvalidOperation:
        raise ExpressionError() 
    except (TypeError, ValueError):
        raise InvalidInputError("Invalid Value: Please use numbers only.")


def compute_pi() -> Decimal:
    with localcontext() as ctx:
        ctx.prec = INTERNAL_PRECISION
        a = Decimal(1)
        b = Decimal(1) / Decimal(2).sqrt()
        t = Decimal(1) / Decimal(4)
        p = Decimal(1)
        for _ in range(7):
            an = (a + b) / 2
            b = (a * b).sqrt()
            t = t - p * (a - an) * (a - an)
            a = an
            p = p * 2
        return (a + b) * (a + b) / (Decimal(4) * t)


PI = compute_pi()
TWO_PI = PI * 2


def _radians(angle: Decimal) -> Decimal:
    return angle * PI / Decimal(180)


def _degrees(rad: Decimal) -> Decimal:
    return rad * Decimal(180) / PI


def _reduce_radians(x: Decimal) -> Decimal:
    y = x % TWO_PI
    if y > PI:
        y -= TWO_PI
    return y


def _sin_decimal(x: Decimal) -> Decimal:
    with localcontext() as ctx:
        ctx.prec = INTERNAL_PRECISION
        x = _reduce_radians(x)
        term = x
        result = Decimal(0)
        n = 1
        eps = Decimal(10) ** (-(INTERNAL_PRECISION - 5))
        while True:
            result += term
            term *= -x * x / (Decimal(2 * n) * Decimal(2 * n + 1))
            if abs(term) < eps:
                break
            n += 1
        return +result


def _cos_decimal(x: Decimal) -> Decimal:
    with localcontext() as ctx:
        ctx.prec = INTERNAL_PRECISION
        x = _reduce_radians(x)
        term = Decimal(1)
        result = Decimal(0)
        n = 1
        eps = Decimal(10) ** (-(INTERNAL_PRECISION - 5))
        while True:
            result += term
            term *= -x * x / (Decimal(2 * n - 1) * Decimal(2 * n))
            if abs(term) < eps:
                break
            n += 1
        return +result


def _atan_decimal(x: Decimal) -> Decimal:
    with localcontext() as ctx:
        ctx.prec = INTERNAL_PRECISION
        if x == 0:
            return Decimal(0)
        if abs(x) > 1:
            sign = Decimal(1) if x > 0 else Decimal(-1)
            return sign * (PI / 2) - _atan_decimal(Decimal(1) / x)
        term = x
        result = term
        n = 1
        eps = Decimal(10) ** (-(INTERNAL_PRECISION - 5))
        while True:
            term *= -x * x * Decimal(2 * n - 1) / Decimal(2 * n + 1)
            if abs(term) < eps:
                break
            result += term
            n += 1
        return +result


def _asin_decimal(x: Decimal) -> Decimal:
    with localcontext() as ctx:
        ctx.prec = INTERNAL_PRECISION
        if x == 0:
            return Decimal(0)
        if abs(x) > 1:
            raise DomainError("Domain Error: Input x must satisfy |x| <= 1")
        if x == 1:
            return PI / 2
        if x == -1:
            return -PI / 2
        return _atan_decimal(x / (Decimal(1) - x * x).sqrt())


def _acos_decimal(x: Decimal) -> Decimal:
    return PI / 2 - _asin_decimal(x)


def _exp_decimal(x: Decimal) -> Decimal:
    return x.exp()


def _ln_decimal(x: Decimal) -> Decimal:
    return x.ln()


def _sinh_decimal(x: Decimal) -> Decimal:
    ex = _exp_decimal(x)
    exn = _exp_decimal(-x)
    return (ex - exn) / 2


def _cosh_decimal(x: Decimal) -> Decimal:
    ex = _exp_decimal(x)
    exn = _exp_decimal(-x)
    return (ex + exn) / 2


def _tanh_decimal(x: Decimal) -> Decimal:
    return _sinh_decimal(x) / _cosh_decimal(x)


def _asinh_decimal(x: Decimal) -> Decimal:
    return _ln_decimal(x + (x * x + 1).sqrt())


def _acosh_decimal(x: Decimal) -> Decimal:
    return _ln_decimal(x + (x - 1).sqrt() * (x + 1).sqrt())


def _atanh_decimal(x: Decimal) -> Decimal:
    return _ln_decimal((1 + x) / (1 - x)) / 2


def get_val() -> Optional[Decimal]:
    """Prompt user for numeric input with error handling.
    
    Returns:
        Decimal if valid, None otherwise
    """
    try:
        val = Decimal(input().strip())
        return val
    except (InvalidOperation, ValueError, TypeError):
        raise InvalidInputError("Invalid Value: Please use numbers only.")


def format_result(result: Decimal | int | str) -> str:
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
            print("\nNo history file found. Try performing a calculation first!")

        history = HISTORY_FILE.read_text(encoding="utf-8").strip()

        if not history:
            print("\nHistory is currently empty.")
        else:
            print("\n--- Scientific Calculation History ---")
            print(history)

    except (PermissionError, UnicodeDecodeError, OSError):
        print("Internal Error: Failed reading history")


def record_history_sci_calc(name: str, val: Decimal | int | str, answer: str) -> None:
    """
    Append calculation to history file.
    
    Args:
        name: Function name
        val: Input val
        answer: Computed result
    """
    try:
        with HISTORY_FILE.open('a', encoding="utf-8") as f:
            f.write(f"{name}({val}) = {answer}\n")
    except (FileNotFoundError, PermissionError, UnicodeDecodeError, OSError):
        print("Internal Error: Failed to record history")

def clear_hist_sci_calc() -> None:
    """Clear all history by truncating the history file."""
    try:
        with HISTORY_FILE.open('w', encoding="utf-8"):
            print("Scientific history cleared successfully!")
    except (FileNotFoundError, PermissionError, UnicodeDecodeError, OSError):
        print("Internal Error: Failed to clear history")


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
        else:
            print("Invalid Choice: Please select 1-6")
            return 0
            

# ============================================================================
# Domain Validators
# ============================================================================

def _validate_trig_asymptote(sub_op_num: int, angle: Decimal | int | str) -> None:
    """
    Check for asymptotes in regular trigonometric functions.
    
    Args:
        sub_op_num: Specific trig function indentifier
        angle: Angle in degrees
    
    Raises:
        AsymptoteError: If angle is at an asymptote
    """
    #cot(x) and cosec(x) undefined where sin(x) = 0 (at n*180°)
    angle_dec = _to_decimal(angle)
    mod_180 = angle_dec % Decimal(180)
    if sub_op_num in (SubOperation.FUNC_4, SubOperation.FUNC_6):
        if abs(mod_180) <= ANGLE_TOLERANCE or abs(mod_180 - Decimal(180)) <= ANGLE_TOLERANCE:
            raise AsymptoteError("Asymptote Error: Division by zero (Asymptote at n*180°)")
    
    # Undefined where cos(x) = 0: tan(x), sec(x)
    if sub_op_num in (SubOperation.FUNC_3, SubOperation.FUNC_5):
        if abs(mod_180 - Decimal(90)) <= ANGLE_TOLERANCE:
            raise AsymptoteError("Asymptote Error: Division by zero (Asymptote at n*180° + 90°)")


def _validate_hyperbolic_asymptote(sub_op_num: int, val: Decimal | int | str) -> None:
    """
    Check for asymptotes in hyperbolic functions.
    
    Args:
        sub_op_num: Specific trig function indentifier
        val: Input val

    Raises:
        AsymptoteError:  If value is at an asymptote
    """
    # coth(0) and cosech(0) are undefined
    val_dec = _to_decimal(val)
    if sub_op_num in (SubOperation.FUNC_4, SubOperation.FUNC_6) and val_dec == 0:
        raise AsymptoteError("Asymptote Error: Division by zero (Undefined at x=0)")


def _validate_inverse_trig_domain(sub_op_num: int, val: Decimal | int | str) -> None:
    """
    Validate domain for inverse trigonometric functions.

    Args:
        sub_op_num: Specific trig function indentifier
        val: Input val

    Raises:
        DomainError: If value is outside valid domain
    """
    # arcsin and arccos require |x| <= 1
    val_dec = _to_decimal(val)
    if sub_op_num in (SubOperation.FUNC_1, SubOperation.FUNC_2):
        if val_dec < -1 or val_dec > 1:
            raise DomainError("Domain Error: Input x must satisfy |x| <= 1")
    
    # arcsec and arccosec require |x| >= 1
    if sub_op_num in (SubOperation.FUNC_5, SubOperation.FUNC_6):
        if -1 < val_dec < 1:
            raise DomainError("Domain Error: Input x must satisfy |x| >= 1")


def _validate_inverse_hyperbolic_domain(sub_op_num: int, val: Decimal | int | str) -> None:
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
        if check_func(_to_decimal(val)):
            raise DomainError(error_msg)


# ============================================================================
# Core Mathematical Functions
# ============================================================================

# Standard Trigonometric Functions (input in degrees)
def sine(angle: Decimal | int | str) -> Decimal: 
    """Calculate sine of angle in degrees."""
    return _sin_decimal(_radians(_to_decimal(angle)))


def cosine(angle: Decimal | int | str) -> Decimal: 
    """Calculate cosine of angle in degrees."""
    return _cos_decimal(_radians(_to_decimal(angle)))


def tangent(angle: Decimal | int | str) -> Decimal: 
    """Calculate tangent of angle in degrees."""
    return _sin_decimal(_radians(_to_decimal(angle))) / _cos_decimal(_radians(_to_decimal(angle)))


def cot(angle: Decimal | int | str) -> Decimal: 
    """Calculate cotangent of angle in degrees."""
    rad = _radians(_to_decimal(angle))
    return _cos_decimal(rad) / _sin_decimal(rad)


def sec(angle: Decimal | int | str) -> Decimal: 
    """Calculate secant of angle in degrees."""
    return Decimal(1) / _cos_decimal(_radians(_to_decimal(angle)))


def cosec(angle: Decimal | int | str) -> Decimal: 
    """Calculate cosecant of angle in degrees."""
    return Decimal(1) / _sin_decimal(_radians(_to_decimal(angle)))


# Inverse Trigonometric Functions (output in degrees)
def sine_inv(val: Decimal | int | str) -> Decimal: 
    """Calculate arcsine, returns result in degrees."""
    return _degrees(_asin_decimal(_to_decimal(val)))


def cosine_inv(val: Decimal | int | str) -> Decimal: 
    """Calculate arccosine, returns result in degrees."""
    return _degrees(_acos_decimal(_to_decimal(val)))


def tangent_inv(val: Decimal | int | str) -> Decimal: 
    """Calculate arctangent, returns result in degrees."""
    return _degrees(_atan_decimal(_to_decimal(val)))


def cot_inv(val: Decimal | int | str) -> Decimal: 
    """Calculate arccotangent, returns result in degrees."""
    return _degrees(_atan_decimal(Decimal(1) / _to_decimal(val)))


def sec_inv(val: Decimal | int | str) -> Decimal: 
    """Calculate arcsecant, returns result in degrees."""
    return _degrees(_acos_decimal(Decimal(1) / _to_decimal(val)))


def cosec_inv(val: Decimal | int | str) -> Decimal: 
    """Calculate arccosecant, returns result in degrees."""
    return _degrees(_asin_decimal(Decimal(1) / _to_decimal(val)))


# Hyperbolic Functions
def sineh(val: Decimal | int | str) -> Decimal:
    """Calculate hyperbolic sine."""
    return _sinh_decimal(_to_decimal(val))


def cosineh(val: Decimal | int | str) -> Decimal:
    """Calculate hyperbolic cosine."""
    return _cosh_decimal(_to_decimal(val))


def tangenth(val: Decimal | int | str) -> Decimal:
    """Calculate hyperbolic tangent."""
    return _tanh_decimal(_to_decimal(val))


def coth(val: Decimal | int | str) -> Decimal:
    """Calculate hyperbolic cotangent."""
    val_dec = _to_decimal(val)
    return _cosh_decimal(val_dec) / _sinh_decimal(val_dec)


def sech(val: Decimal | int | str) -> Decimal:
    """Calculate hyperbolic secant."""
    return Decimal(1) / _cosh_decimal(_to_decimal(val))


def cosech(val: Decimal | int | str) -> Decimal:
    """Calculate hyperbolic cosecant."""
    return Decimal(1) / _sinh_decimal(_to_decimal(val))


# Inverse Hyperbolic Functions
def sineh_inv(val: Decimal | int | str) -> Decimal:
    """Calculate inverse hyperbolic sine."""
    return _asinh_decimal(_to_decimal(val))


def cosineh_inv(val: Decimal | int | str) -> Decimal:
    """Calculate inverse hyperbolic cosine."""
    return _acosh_decimal(_to_decimal(val))


def tangenth_inv(val: Decimal | int | str) -> Decimal:
    """Calculate inverse hyperbolic tangent."""
    return _atanh_decimal(_to_decimal(val))


def coth_inv(val: Decimal | int | str) -> Decimal:
    """Calculate inverse hyperbolic cotangent."""
    val_dec = _to_decimal(val)
    return _atanh_decimal(Decimal(1) / val_dec)


def sech_inv(val: Decimal | int | str) -> Decimal:
    """Calculate inverse hyperbolic secant."""
    return _acosh_decimal(Decimal(1) / _to_decimal(val))


def cosech_inv(val: Decimal | int | str) -> Decimal:
    """Calculate inverse hyperbolic cosecant."""
    return _asinh_decimal(Decimal(1) / _to_decimal(val))


# ============================================================================
# Function Registry
# ============================================================================

#Dictionary mapping (category, sub_op) tuples to (name, function) pairs
trigo_funcs: dict[Tuple[int, int], Tuple[str, Callable[[Decimal | int | str], Decimal]]]= {
    # Standard Trigonometric
    (FunctionCategory.TRIGONOMETRIC, SubOperation.FUNC_1): ("sin", sine),
    (FunctionCategory.TRIGONOMETRIC, SubOperation.FUNC_2): ("cos", cosine),
    (FunctionCategory.TRIGONOMETRIC, SubOperation.FUNC_3): ("tan", tangent),
    (FunctionCategory.TRIGONOMETRIC, SubOperation.FUNC_4): ("cot", cot),
    (FunctionCategory.TRIGONOMETRIC, SubOperation.FUNC_5): ("sec", sec),
    (FunctionCategory.TRIGONOMETRIC, SubOperation.FUNC_6): ("cosec", cosec),

    # Hyperbolic
    (FunctionCategory.HYPERBOLIC, SubOperation.FUNC_1): ("sinh", sineh),
    (FunctionCategory.HYPERBOLIC, SubOperation.FUNC_2): ("cosh", cosineh),
    (FunctionCategory.HYPERBOLIC, SubOperation.FUNC_3): ("tanh", tangenth),
    (FunctionCategory.HYPERBOLIC, SubOperation.FUNC_4): ("coth", coth),
    (FunctionCategory.HYPERBOLIC, SubOperation.FUNC_5): ("sech", sech),
    (FunctionCategory.HYPERBOLIC, SubOperation.FUNC_6): ("cosech", cosech),

    # Inverse Trigonometric
    (FunctionCategory.INVERSE_TRIGONOMETRIC, SubOperation.FUNC_1): ("sin⁻¹", sine_inv),
    (FunctionCategory.INVERSE_TRIGONOMETRIC, SubOperation.FUNC_2): ("cos⁻¹", cosine_inv),
    (FunctionCategory.INVERSE_TRIGONOMETRIC, SubOperation.FUNC_3): ("tan⁻¹", tangent_inv),
    (FunctionCategory.INVERSE_TRIGONOMETRIC, SubOperation.FUNC_4): ("cot⁻¹", cot_inv),
    (FunctionCategory.INVERSE_TRIGONOMETRIC, SubOperation.FUNC_5): ("sec⁻¹", sec_inv),
    (FunctionCategory.INVERSE_TRIGONOMETRIC, SubOperation.FUNC_6): ("cosec⁻¹", cosec_inv),

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
        func: Callable[[Decimal], Decimal],
        val: Decimal | int | str
) -> str:
    """
    Validate input domain and execute scientific calculation.
    
    This function performs domain validation before computation  to ensure
    mathematical correctness and provide meaningful error messages.
    
    Args:
        op_num: Category of function (Trigonometric, Hyperbolic, etc.)
        sub_op_num: Specific function identifier within category
        name: Display name of the function
        func: The mathematical function to execute
        val: The input value/angle
    
    Returns:
        Formatted result string or descriptive error message
    """
    try:
        # Perform domain validation based on function category
        if op_num == FunctionCategory.TRIGONOMETRIC:
            _validate_trig_asymptote(sub_op_num, val)

        elif op_num == FunctionCategory.HYPERBOLIC:
            _validate_hyperbolic_asymptote(sub_op_num, val)
        
        elif op_num == FunctionCategory.INVERSE_TRIGONOMETRIC:
            _validate_inverse_trig_domain(sub_op_num, val)
            if sub_op_num == SubOperation.FUNC_4 and _to_decimal(val) == 0:
                return f"{name}({val}) = 90"

        elif op_num == FunctionCategory.INVERSE_HYPERBOLIC:
            _validate_inverse_hyperbolic_domain(sub_op_num, val)

        # Execute calculation and format result
        result = func(_to_decimal(val))
        formatted_result = format_result(result)
        record_history_sci_calc(name, val, formatted_result)
        return f"{name}({val}) = {formatted_result}"
    
    except CalculatorError as e:
        return str(e)
    
    except (ValueError, ArithmeticError):
        return f"Math Error: {e}"
    
    except Exception as e:
        return f"System Error: {type(e).__name__}"


def eval_trigo_func(key: Tuple[int, int]) -> None:
    """
    Evaluate trigonometric function based on user input.
    
    Args:
        key: Tuple of (category, sub_operation) identifying the function
    """
    try:
        if key not in trigo_funcs:
            print("Invalid Key Error: Please select a correct pair of main_menu and sub_menu options.")
        
        op_num, sub_op_num = key
        name, func = trigo_funcs[key]

        print("Enter angle:" if op_num == FunctionCategory.TRIGONOMETRIC else "Enter value: ", end='')
        val = get_val()
        if val is not None:
            answer = validate_and_eval(op_num, sub_op_num, name, func, val)
            print(answer)

    except CalculatorError:
        raise

    except Exception:
        raise


# ============================================================================
# Main User interface function
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
                print("Invalid Input: Please select 1-9")

        except CalculatorError as e:
            print(e)
            continue

        except (ValueError, TypeError):
            print("Invalid input: Please use numbers only.")
            continue

        except Exception:
            print(f"System Error: {type(e).__name__}")
            continue

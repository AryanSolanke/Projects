"""
Angle Converter Module

Provides angle conversion functionality using Decimal arithmetic.
Supports degree, radian, and gradian conversions.
"""

from decimal import Decimal, localcontext
from typing import Tuple, Callable, Dict
from enum import IntEnum

from calculator.standard import errmsg
from calculator.converters.utils import get_numeric_input, format_numeric_result, to_decimal

INTERNAL_PRECISION = 60


def _compute_pi() -> Decimal:
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


PI = _compute_pi()


class AngleUnit(IntEnum):
    """Angle unit types."""
    DEGREE = 1
    RADIAN = 2
    GRADIAN = 3
    QUIT = 4


# ============================================================================
# Menu Display Functions
# ============================================================================

def angle_conversion_menuMsg() -> None:
    """Display angle conversion menu."""
    print("\n" + "="*50)
    print("ANGLE CONVERSION")
    print("="*50)
    print("1. Degree (°)")
    print("2. Radian (rad)")
    print("3. Gradian (grad)")
    print("4. Quit Angle Converter")
    print("="*50)


# ============================================================================
# Angle Conversion Functions (pure Decimal)
# ============================================================================

def to_rads(angle: Decimal) -> Decimal:
    """Convert degrees to radians."""
    return to_decimal(angle, "Angle") * PI / Decimal(180)


def to_deg(angle: Decimal) -> Decimal:
    """Convert radians to degrees."""
    return to_decimal(angle, "Angle") * Decimal(180) / PI


def to_grad(angle: Decimal) -> Decimal:
    """Convert degrees to gradians."""
    return to_decimal(angle, "Angle") * Decimal(200) / Decimal(180)


def convert_angle(
    name1: str,
    func1: Callable[[Decimal], Decimal],
    name2: str,
    func2: Callable[[Decimal], Decimal],
    angle: Decimal,
) -> Tuple[str, str]:
    """
    Convert angles to two different units.

    Args:
        name1: Name of first output unit
        func1: Conversion function for first unit
        name2: Name of second output unit
        func2: Conversion function for second unit
        angle: Input angle value

    Returns:
        Tuple of two formatted conversion results
    """
    ans1 = f"{name1}({angle}) = {format_numeric_result(func1(angle))}"
    ans2 = f"{name2}({angle}) = {format_numeric_result(func2(angle))}"
    return ans1, ans2


# ============================================================================
# Conversion Lookup Tables
# ============================================================================

angle_conv_choices = ["Degree", "Radians", "Gradians"]

# Angle conversion configurations: (output1_name, func1, output2_name, func2)
angle_conv_funcs: Dict[int, Tuple[str, Callable, str, Callable]] = {
    AngleUnit.DEGREE: ("rad", to_rads, "grad", to_grad),
    AngleUnit.RADIAN: ("deg", to_deg, "grad", to_grad),
    AngleUnit.GRADIAN: ("deg", to_deg, "rad", to_rads),
}


# ============================================================================
# Main Angle Converter Function
# ============================================================================

def angle_converter() -> None:
    """Main angle conversion interface."""
    try:
        angle_conversion_menuMsg()
        choice = int(input("\nEnter your choice: "))

        if choice == AngleUnit.QUIT:
            return

        if choice in angle_conv_funcs:
            name1, func1, name2, func2 = angle_conv_funcs[choice]
            unit_name = angle_conv_choices[choice - 1]
            print(f"\nEnter angle in {unit_name}: ", end="")
            angle = get_numeric_input()

            if angle is not None:
                ans1, ans2 = convert_angle(name1, func1, name2, func2, angle)
                print(f"\n   {ans1}")
                print(f"   {ans2}\n")
            else:
                print("No angle given\n")
        else:
            print("Invalid choice. Please select 1-3\n")

    except (TypeError, UnboundLocalError, SyntaxError, ValueError):
        errmsg()

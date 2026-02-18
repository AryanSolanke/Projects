"""
Temperature Converter Module

Provides temperature conversion functionality.
Supports Celsius, Kelvin, and Fahrenheit conversions.
"""

from decimal import Decimal
from enum import IntEnum
from typing import Callable, Dict, Tuple

from std import errmsg
from sci import get_val

def _to_decimal(value: float | int | Decimal) -> Decimal:
    if isinstance(value, Decimal):
        return value
    if isinstance(value, (int, float)):
        return Decimal(str(value))
    raise TypeError("Temperature value must be numeric.")


class TempUnit(IntEnum):
    """Temperature unit types."""
    CELSIUS = 1
    KELVIN = 2
    FAHRENHEIT = 3
    QUIT = 4


# ============================================================================
# Menu Display Functions
# ============================================================================

def temp_conv_menuMsg() -> None:
    """Display temperature conversion menu."""
    print("\n" + "="*50)
    print("TEMPERATURE CONVERSION")
    print("="*50)
    print("1. Celsius (°C)")
    print("2. Kelvin (K)")
    print("3. Fahrenheit (°F)")
    print("4. Quit Temperature Converter")
    print("="*50)


# ============================================================================
# Temperature Conversion Functions
# ============================================================================

def C_to_kelvin(tmp: float) -> Decimal:
    """Convert Celsius to Kelvin."""
    return _to_decimal(tmp) + Decimal("273.15")


def C_to_Fahrenheit(tmp: float) -> Decimal:
    """Convert Celsius to Fahrenheit."""
    return (_to_decimal(tmp) * Decimal(9) / Decimal(5)) + Decimal(32)


def K_to_celsius(tmp: float) -> Decimal:
    """Convert Kelvin to Celsius."""
    return _to_decimal(tmp) - Decimal("273.15")


def K_to_Fahrenheit(tmp: float) -> Decimal:
    """Convert Kelvin to Fahrenheit."""
    return C_to_Fahrenheit(K_to_celsius(tmp))


def F_to_celsius(tmp: float) -> float:
    """Convert Fahrenheit to Celsius."""
    return (_to_decimal(tmp) - Decimal(32)) * Decimal(5) / Decimal(9)


def F_to_kelvin(tmp: float) -> Decimal:
    """Convert Fahrenheit to Kelvin."""
    return _to_decimal(F_to_celsius(tmp)) + Decimal("273.15")


# ============================================================================
# Conversion Lookup Tables
# ============================================================================

# Temperature conversion: (from_unit, to_unit) -> (from_name, to_name, conversion_function)
temp_conv_funcs: Dict[Tuple[int, int], Tuple[str, str, Callable]] = {
    (TempUnit.CELSIUS, TempUnit.KELVIN): ("Celsius", "Kelvin", C_to_kelvin),
    (TempUnit.CELSIUS, TempUnit.FAHRENHEIT): ("Celsius", "Fahrenheit", C_to_Fahrenheit),
    (TempUnit.KELVIN, TempUnit.CELSIUS): ("Kelvin", "Celsius", K_to_celsius),
    (TempUnit.KELVIN, TempUnit.FAHRENHEIT): ("Kelvin", "Fahrenheit", K_to_Fahrenheit),
    (TempUnit.FAHRENHEIT, TempUnit.CELSIUS): ("Fahrenheit", "Celsius", F_to_celsius),
    (TempUnit.FAHRENHEIT, TempUnit.KELVIN): ("Fahrenheit", "Kelvin", F_to_kelvin),
}


# ============================================================================
# Main Temperature Converter Function
# ============================================================================

def temperature_converter() -> None:
    """Main temperature conversion interface."""
    try:
        temp_conv_menuMsg()
        input_choice = int(input("\nEnter input unit (1-3): "))

        if input_choice == TempUnit.QUIT:
            return

        output_choice = int(input("Enter output unit (1-3): "))

        if output_choice == TempUnit.QUIT:
            return

        key = (input_choice, output_choice)

        if key in temp_conv_funcs:
            print("\nEnter temperature: ", end="")
            input_tmp = get_val()

            if input_tmp is not None:
                from_tmp, to_tmp, tmp_func = temp_conv_funcs[key]
                result = tmp_func(input_tmp)
                print(f"\n   {input_tmp} {from_tmp} = {result} {to_tmp}\n")
            else:
                errmsg()
        else:
            errmsg()

    except (TypeError, UnboundLocalError, SyntaxError, ValueError):
        errmsg()

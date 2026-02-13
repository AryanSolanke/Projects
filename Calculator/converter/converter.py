"""
Converter Module

Provides angle, temperature, weight, and pressure conversion functionality.
Routes to specific converter modules.
"""

from enum import IntEnum

from std import errmsg

# Angle conversions
from converter.angle_converter import (
    AngleUnit,
    angle_converter as run_angle_converter,
)

# Temperature conversions
from converter.temp_converter import (
    TempUnit,
    temperature_converter,
)

# Weight conversions
from converter.weight_converter import (
    WeightUnit,
    weight_converter,
)

# Pressure conversions
from converter.pressure_converter import (
    PressureUnit,
    pressure_converter,
)


class MenuOptions(IntEnum):
    """Conversion unit types."""
    ANGLE_CONVERSION = 1
    TEMPERATURE_CONVERSION = 2
    WEIGHT_CONVERSION = 3
    PRESSURE_CONVERSION = 4
    QUIT = 5


# ============================================================================
# Menu Display Functions
# ============================================================================

def converter_menuMsg() -> None:
    """Display main converter menu."""
    print("\n|=====>Convertion Operations<=====|\n")
    print("1. Angle.\n2. Temperature.\n3. Weight.\n4. Pressure.\n5. Quit Converter.")


# ============================================================================
# Main Converter Function
# ============================================================================

def converter_menu() -> None:
    """Main converter interface. Routes to specific converter modules."""
    while True:
        try:
            converter_menuMsg()
            op_num = int(input("Enter your choice: "))

            if op_num == MenuOptions.QUIT:
                print("\nConverter menu closed\n")
                break

            if op_num == MenuOptions.ANGLE_CONVERSION:
                run_angle_converter()
            elif op_num == MenuOptions.TEMPERATURE_CONVERSION:
                temperature_converter()
            elif op_num == MenuOptions.WEIGHT_CONVERSION:
                weight_converter()
            elif op_num == MenuOptions.PRESSURE_CONVERSION:
                pressure_converter()
            else:
                errmsg()

        except (TypeError, UnboundLocalError, SyntaxError, ValueError):
            errmsg()
            continue


def angle_converter() -> None:
    """Backward-compatible entry point for the full converter menu."""
    converter_menu()

"""
Pressure Converter Module

Provides pressure conversion functionality.
Supports comprehensive bidirectional conversions for all units.
"""

from enum import IntEnum

from std import errmsg
from sci import get_val, format_result


class PressureUnit(IntEnum):
    """Pressure unit types - 6 units total."""
    ATMOSPHERE = 1
    BAR = 2
    KILOPASCAL = 3
    MM_MERCURY = 4
    PASCAL = 5
    PSI = 6
    QUIT = 7


# ============================================================================
# Menu Display Functions
# ============================================================================

def pressure_conv_menuMsg() -> None:
    """Display pressure conversion menu with all 6 units."""
    print("\n" + "="*50)
    print("🌡️  PRESSURE CONVERSION")
    print("="*50)
    print("\n💨 PRESSURE UNITS:")
    print("  1. Atmosphere (atm)")
    print("  2. Bar (bar)")
    print("  3. Kilopascal (kPa)")
    print("  4. Millimeter of Mercury (mmHg)")
    print("  5. Pascal (Pa)")
    print("  6. Pounds per Square Inch (psi)")
    print("\n  7. Quit Pressure Converter")
    print("="*50)


# ============================================================================
# Universal Pressure Conversion Function
# ============================================================================

def convert_pressure(value: float, from_unit: int, to_unit: int) -> float:
    """
    Universal pressure converter - converts ANY pressure unit to ANY other pressure unit.

    Strategy:
    1. Convert input value to Pascals (base unit)
    2. Convert Pascals to target unit

    Args:
        value: Pressure value to convert
        from_unit: Source unit (PressureUnit enum value)
        to_unit: Target unit (PressureUnit enum value)

    Returns:
        Converted pressure value as float
    """
    to_pascal_factors = {
        PressureUnit.ATMOSPHERE: 101325.0,
        PressureUnit.BAR: 100000.0,
        PressureUnit.KILOPASCAL: 1000.0,
        PressureUnit.MM_MERCURY: 133.322,
        PressureUnit.PASCAL: 1.0,
        PressureUnit.PSI: 6894.76,
    }

    pressure_in_pa = value * to_pascal_factors[from_unit]
    return pressure_in_pa / to_pascal_factors[to_unit]


# ============================================================================
# Pressure Unit Names and Abbreviations
# ============================================================================

PRESSURE_UNIT_NAMES = {
    PressureUnit.ATMOSPHERE: "Atmosphere",
    PressureUnit.BAR: "Bar",
    PressureUnit.KILOPASCAL: "Kilopascal",
    PressureUnit.MM_MERCURY: "Millimeter of Mercury",
    PressureUnit.PASCAL: "Pascal",
    PressureUnit.PSI: "Pounds per Square Inch",
}

PRESSURE_UNIT_ABBREV = {
    PressureUnit.ATMOSPHERE: "atm",
    PressureUnit.BAR: "bar",
    PressureUnit.KILOPASCAL: "kPa",
    PressureUnit.MM_MERCURY: "mmHg",
    PressureUnit.PASCAL: "Pa",
    PressureUnit.PSI: "psi",
}


# ============================================================================
# Main Pressure Converter Function
# ============================================================================

def pressure_converter() -> None:
    """Main pressure conversion interface."""
    try:
        pressure_conv_menuMsg()
        input_choice = int(input("\n➤ Enter FROM unit (1-6): "))

        if input_choice == PressureUnit.QUIT:
            return

        if input_choice not in PRESSURE_UNIT_NAMES:
            print("❌ Invalid choice. Please select 1-6.")
            return

        output_choice = int(input("➤ Enter TO unit (1-6): "))

        if output_choice == PressureUnit.QUIT:
            return

        if output_choice not in PRESSURE_UNIT_NAMES:
            print("❌ Invalid choice. Please select 1-6.")
            return

        if input_choice == output_choice:
            print("\n⚠️  Input and output units are the same. No conversion needed.\n")
            return

        print("\n💨 Enter pressure: ", end="")
        input_pressure = get_val()

        if input_pressure is not None:
            from_unit_name = PRESSURE_UNIT_NAMES[input_choice]
            to_unit_name = PRESSURE_UNIT_NAMES[output_choice]
            from_abbrev = PRESSURE_UNIT_ABBREV[input_choice]
            to_abbrev = PRESSURE_UNIT_ABBREV[output_choice]

            result = convert_pressure(input_pressure, input_choice, output_choice)

            print("\n" + "="*50)
            print("   CONVERSION RESULT:")
            print(f"   {input_pressure} {from_abbrev} = {format_result(result)} {to_abbrev}")
            print(f"   ({from_unit_name} → {to_unit_name})")
            print("="*50 + "\n")
        else:
            errmsg()

    except (TypeError, UnboundLocalError, SyntaxError, ValueError):
        errmsg()

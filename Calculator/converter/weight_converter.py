"""
Weight Converter Module

Provides weight conversion functionality.
Supports comprehensive bidirectional conversions for all units.
"""

from decimal import Decimal
from enum import IntEnum

from std import errmsg
from sci import get_val, format_result

def _to_decimal(value: float | int | Decimal) -> Decimal:
    if isinstance(value, Decimal):
        return value
    if isinstance(value, (int, float)):
        return Decimal(str(value))
    raise TypeError("Weight value must be numeric.")


class WeightUnit(IntEnum):
    """Weight unit types - 13 units total."""
    KILOGRAM = 1
    GRAM = 2
    MILLIGRAM = 3
    CENTIGRAM = 4
    DECIGRAM = 5
    DECAGRAM = 6
    HECTOGRAM = 7
    METRIC_TONNE = 8
    OUNCE = 9
    POUND = 10
    STONE = 11
    SHORT_TON_US = 12
    LONG_TON_UK = 13
    QUIT = 14


# ============================================================================
# Menu Display Functions
# ============================================================================

def weight_conv_menuMsg() -> None:
    """Display weight conversion menu with all 13 units."""
    print("\n" + "="*50)
    print("WEIGHT CONVERSION")
    print("="*50)
    print("\nMETRIC UNITS:")
    print("  1.  Kilogram (kg)")
    print("  2.  Gram (g)")
    print("  3.  Milligram (mg)")
    print("  4.  Centigram (cg)")
    print("  5.  Decigram (dg)")
    print("  6.  Decagram (dag)")
    print("  7.  Hectogram (hg)")
    print("  8.  Metric Tonne (t)")
    print("\nIMPERIAL/US UNITS:")
    print("  9.  Ounce (oz)")
    print("  10. Pound (lb)")
    print("  11. Stone (st)")
    print("  12. Short Ton - US (ton)")
    print("  13. Long Ton - UK (ton)")
    print("\n  14. Quit Weight Converter")
    print("="*50)


# ============================================================================
# Universal Weight Conversion Function
# ============================================================================

def convert_weight(value: float, from_unit: int, to_unit: int) -> Decimal:
    """
    Universal weight converter - converts ANY weight unit to ANY other weight unit.

    Strategy:
    1. Convert input value to kilograms (base unit)
    2. Convert kilograms to target unit

    Args:
        value: Weight value to convert
        from_unit: Source unit (WeightUnit enum value)
        to_unit: Target unit (WeightUnit enum value)

    Returns:
        Converted weight value as float
    """
    to_kg_factors = {
        WeightUnit.KILOGRAM: Decimal("1"),
        WeightUnit.GRAM: Decimal("0.001"),
        WeightUnit.MILLIGRAM: Decimal("0.000001"),
        WeightUnit.CENTIGRAM: Decimal("0.00001"),
        WeightUnit.DECIGRAM: Decimal("0.0001"),
        WeightUnit.DECAGRAM: Decimal("0.01"),
        WeightUnit.HECTOGRAM: Decimal("0.1"),
        WeightUnit.METRIC_TONNE: Decimal("1000"),
        WeightUnit.OUNCE: Decimal("0.0283495"),
        WeightUnit.POUND: Decimal("0.453592"),
        WeightUnit.STONE: Decimal("6.35029"),
        WeightUnit.SHORT_TON_US: Decimal("907.185"),
        WeightUnit.LONG_TON_UK: Decimal("1016.05"),
    }

    weight_in_kg = _to_decimal(value) * to_kg_factors[from_unit]
    return weight_in_kg / to_kg_factors[to_unit]


# ============================================================================
# Weight Unit Names and Abbreviations
# ============================================================================

WEIGHT_UNIT_NAMES = {
    WeightUnit.KILOGRAM: "Kilogram",
    WeightUnit.GRAM: "Gram",
    WeightUnit.MILLIGRAM: "Milligram",
    WeightUnit.CENTIGRAM: "Centigram",
    WeightUnit.DECIGRAM: "Decigram",
    WeightUnit.DECAGRAM: "Decagram",
    WeightUnit.HECTOGRAM: "Hectogram",
    WeightUnit.METRIC_TONNE: "Metric Tonne",
    WeightUnit.OUNCE: "Ounce",
    WeightUnit.POUND: "Pound",
    WeightUnit.STONE: "Stone",
    WeightUnit.SHORT_TON_US: "Short Ton (US)",
    WeightUnit.LONG_TON_UK: "Long Ton (UK)",
}

WEIGHT_UNIT_ABBREV = {
    WeightUnit.KILOGRAM: "kg",
    WeightUnit.GRAM: "g",
    WeightUnit.MILLIGRAM: "mg",
    WeightUnit.CENTIGRAM: "cg",
    WeightUnit.DECIGRAM: "dg",
    WeightUnit.DECAGRAM: "dag",
    WeightUnit.HECTOGRAM: "hg",
    WeightUnit.METRIC_TONNE: "t",
    WeightUnit.OUNCE: "oz",
    WeightUnit.POUND: "lb",
    WeightUnit.STONE: "st",
    WeightUnit.SHORT_TON_US: "ton (US)",
    WeightUnit.LONG_TON_UK: "ton (UK)",
}


# ============================================================================
# Main Weight Converter Function
# ============================================================================

def weight_converter() -> None:
    """Main weight conversion interface."""
    try:
        weight_conv_menuMsg()
        input_choice = int(input("\nEnter FROM unit (1-13): "))

        if input_choice == WeightUnit.QUIT:
            return

        if input_choice not in WEIGHT_UNIT_NAMES:
            print("Invalid choice. Please select 1-13.")
            return

        output_choice = int(input("Enter TO unit (1-13): "))

        if output_choice == WeightUnit.QUIT:
            return

        if output_choice not in WEIGHT_UNIT_NAMES:
            print("Invalid choice. Please select 1-13.")
            return

        if input_choice == output_choice:
            print("\nInput and output units are the same. No conversion needed.\n")
            return

        print("\nEnter weight: ", end="")
        input_weight = get_val()

        if input_weight is not None:
            from_unit_name = WEIGHT_UNIT_NAMES[input_choice]
            to_unit_name = WEIGHT_UNIT_NAMES[output_choice]
            from_abbrev = WEIGHT_UNIT_ABBREV[input_choice]
            to_abbrev = WEIGHT_UNIT_ABBREV[output_choice]

            result = convert_weight(input_weight, input_choice, output_choice)

            print("\n" + "="*50)
            print("   CONVERSION RESULT:")
            print(f"   {input_weight} {from_abbrev} = {format_result(result)} {to_abbrev}")
            print(f"   ({from_unit_name} -> {to_unit_name})")
            print("="*50 + "\n")
        else:
            errmsg()

    except (TypeError, UnboundLocalError, SyntaxError, ValueError):
        errmsg()

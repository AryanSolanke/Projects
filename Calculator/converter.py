"""
Converter Module

Provides angle, temperature, weight, and pressure conversion functionality.
Supports comprehensive bidirectional conversions for all units.
"""

from math import radians, degrees, log
from typing import Tuple, Callable, Dict, Optional
from enum import IntEnum

# Import from modules
from std import errmsg
from sci import get_val, format_result

class AngleUnit(IntEnum):
    """Angle unit types."""
    DEGREE = 1
    RADIAN = 2
    GRADIAN = 3
    QUIT = 4

class TempUnit(IntEnum):
    """Temperature unit types."""
    CELSIUS = 1
    KELVIN = 2
    FAHRENHEIT = 3
    QUIT = 4

class WeightUnit(IntEnum):
    """Weight unit types - 14 units total."""
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

class PressureUnit(IntEnum):
    """Pressure unit types - 6 units total."""
    ATMOSPHERE = 1
    BAR = 2
    KILOPASCAL = 3
    MM_MERCURY = 4
    PASCAL = 5
    PSI = 6
    QUIT = 7

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

def angle_conversion_menuMsg() -> None:
    """Display angle conversion menu."""
    print("\n|=====>Input choices<=====|\n")
    print("Select a input choice\n")
    print("1. Degree.\n2. Radians \n3. Gradians\n4. Quit Angle Converter.")

def temp_conv_menuMsg() -> None:
    """Display temperature conversion menu."""
    print("\n|=====>Input choices<=====|\n")
    print("Select a input choice\n")
    print("1. Celsius.\n2. Kelvin \n3. Fahrenheit\n4. Quit Temperature Converter.")

def weight_conv_menuMsg() -> None:
    """Display weight conversion menu with all 14 units."""
    print("\n" + "="*50)
    print("           WEIGHT UNIT CONVERSION MENU")
    print("="*50)
    print("\n📊 METRIC UNITS:")
    print("  1.  Kilogram (kg)")
    print("  2.  Gram (g)")
    print("  3.  Milligram (mg)")
    print("  4.  Centigram (cg)")
    print("  5.  Decigram (dg)")
    print("  6.  Decagram (dag)")
    print("  7.  Hectogram (hg)")
    print("  8.  Metric Tonne (t)")
    print("\n⚖️  IMPERIAL/US UNITS:")
    print("  9.  Ounce (oz)")
    print("  10. Pound (lb)")
    print("  11. Stone (st)")
    print("  12. Short Ton - US (ton)")
    print("  13. Long Ton - UK (ton)")
    print("\n  14. Quit Weight Converter")
    print("="*50)

def pressure_conv_menuMsg() -> None:
    """Display pressure conversion menu with all 6 units."""
    print("\n" + "="*50)
    print("         PRESSURE UNIT CONVERSION MENU")
    print("="*50)
    print("\n🌡️  PRESSURE UNITS:")
    print("  1. Atmosphere (atm)")
    print("  2. Bar (bar)")
    print("  3. Kilopascal (kPa)")
    print("  4. Millimeter of Mercury (mmHg)")
    print("  5. Pascal (Pa)")
    print("  6. Pounds per Square Inch (psi)")
    print("\n  7. Quit Pressure Converter")
    print("="*50)


# ============================================================================
# Angle Conversion Functions
# ============================================================================

def to_rads(angle: float) -> float:
    """Convert degrees to radians"""
    return radians(angle)


def to_deg(angle: float) -> float: 
    """Convert radians to degrees"""
    return degrees(angle)


def to_grad(angle: float) -> float: 
    """Convert degrees to gradians"""
    return (angle*200)/180


def convert_angle(
        name1: str,
        func1: Callable[[float], float],
        name2: str,
        func2: Callable[[float], float],
        angle: float
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
    ans1 = f"{name1}({angle}) = {format_result(func1(angle))}"
    ans2 = f"{name2}({angle}) = {format_result(func2(angle))}"
    return ans1, ans2


# ============================================================================
# Temperature Conversion Functions
# ============================================================================

def C_to_kelvin(tmp: float) -> float:
    """Converts Celsius to Kelvin."""
    return (tmp+273.15)


def C_to_Fahrenheit(tmp: float) -> float:
    """Converts Celsius to Fahrenheit."""
    return ((9/5)*tmp) + 32


def K_to_celsius(tmp: float) -> float:
    """Converts Kelvin to Celsius."""
    return (tmp-273.15)


def K_to_Fahrenheit(tmp: float) -> float:
    """Converts Kelvin to Fahrenheit."""
    return C_to_Fahrenheit(K_to_celsius(tmp))


def F_to_celsius(tmp: float) -> float:
    """Converts Fahrenheit to Celsius"""
    return (5/9)*(tmp - 32)


def F_to_kelvin(tmp: float) -> float:
    """Converts Fahrenheit to Kelvin"""
    return F_to_celsius(tmp) + 273.15


# ============================================================================
# Universal Weight Conversion Function
# ============================================================================

def convert_weight(value: float, from_unit: int, to_unit: int) -> float:
    """
    Universal weight converter - converts ANY weight unit to ANY other weight unit.
    
    This single function handles ALL 182 possible conversions (14×13 pairs).
    
    Strategy: 
    1. Convert input value to kilograms (base unit)
    2. Convert kilograms to target unit
    
    Conversion factors (to kilograms):
    --------------------------------
    Metric System:
    - 1 Kilogram    = 1 kg
    - 1 Gram        = 0.001 kg
    - 1 Milligram   = 0.000001 kg (1e-6)
    - 1 Centigram   = 0.00001 kg (1e-5)
    - 1 Decigram    = 0.0001 kg (1e-4)
    - 1 Decagram    = 0.01 kg
    - 1 Hectogram   = 0.1 kg
    - 1 Metric Tonne= 1000 kg
    
    Imperial/US System:
    - 1 Ounce       = 0.0283495 kg
    - 1 Pound       = 0.453592 kg
    - 1 Stone       = 6.35029 kg
    - 1 Short Ton   = 907.185 kg
    - 1 Long Ton    = 1016.05 kg
    
    Args:
        value: Weight value to convert
        from_unit: Source unit (WeightUnit enum value)
        to_unit: Target unit (WeightUnit enum value)
    
    Returns:
        Converted weight value as float
    """
    # Conversion factors: Each unit -> kilograms
    to_kg_factors = {
        WeightUnit.KILOGRAM: 1.0,
        WeightUnit.GRAM: 0.001,
        WeightUnit.MILLIGRAM: 0.000001,
        WeightUnit.CENTIGRAM: 0.00001,
        WeightUnit.DECIGRAM: 0.0001,
        WeightUnit.DECAGRAM: 0.01,
        WeightUnit.HECTOGRAM: 0.1,
        WeightUnit.METRIC_TONNE: 1000.0,
        WeightUnit.OUNCE: 0.0283495,
        WeightUnit.POUND: 0.453592,
        WeightUnit.STONE: 6.35029,
        WeightUnit.SHORT_TON_US: 907.185,
        WeightUnit.LONG_TON_UK: 1016.05,
    }
    
    # Step 1: Convert input value to kilograms (base unit)
    weight_in_kg = value * to_kg_factors[from_unit]
    
    # Step 2: Convert kilograms to target unit
    result = weight_in_kg / to_kg_factors[to_unit]
    
    return result


# ============================================================================
# Universal Pressure Conversion Function
# ============================================================================

def convert_pressure(value: float, from_unit: int, to_unit: int) -> float:
    """
    Universal pressure converter - converts ANY pressure unit to ANY other pressure unit.
    
    This single function handles ALL 30 possible conversions (6×5 pairs).
    
    Strategy:
    1. Convert input value to Pascals (base unit)
    2. Convert Pascals to target unit
    
    Conversion factors (to Pascals):
    --------------------------------
    - 1 Atmosphere (atm)        = 101325 Pa
    - 1 Bar                     = 100000 Pa
    - 1 Kilopascal (kPa)        = 1000 Pa
    - 1 Millimeter of Mercury   = 133.322 Pa
    - 1 Pascal (Pa)             = 1 Pa
    - 1 Pounds per Square Inch  = 6894.76 Pa
    
    Args:
        value: Pressure value to convert
        from_unit: Source unit (PressureUnit enum value)
        to_unit: Target unit (PressureUnit enum value)
    
    Returns:
        Converted pressure value as float
    
    Examples:
        >>> convert_pressure(1, PressureUnit.ATMOSPHERE, PressureUnit.BAR)
        1.01325
        >>> convert_pressure(1, PressureUnit.PSI, PressureUnit.KILOPASCAL)
        6.89476
    """
    # Conversion factors: Each unit -> Pascals
    to_pascal_factors = {
        PressureUnit.ATMOSPHERE: 101325.0,
        PressureUnit.BAR: 100000.0,
        PressureUnit.KILOPASCAL: 1000.0,
        PressureUnit.MM_MERCURY: 133.322,
        PressureUnit.PASCAL: 1.0,
        PressureUnit.PSI: 6894.76,
    }
    
    # Step 1: Convert input value to Pascals (base unit)
    pressure_in_pa = value * to_pascal_factors[from_unit]
    
    # Step 2: Convert Pascals to target unit
    result = pressure_in_pa / to_pascal_factors[to_unit]
    
    return result


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
# Conversion Lookup Tables
# ============================================================================

angle_conv_choices = ['Degree', 'Radians', 'Gradians']

# Angle conversion configurations: (output1_name, func1, output2_name, func2) 
angle_conv_funcs: Dict[int, Tuple[str, Callable, str, Callable]]= {
    AngleUnit.DEGREE: ("rad", to_rads, "grad", to_grad),
    AngleUnit.RADIAN: ("deg", to_deg, "grad", to_grad),
    AngleUnit.GRADIAN: ("deg", to_deg, "rad", to_rads)
    }

# Temperature conversion: (from_unit, to_unit, conversion_function)
temp_conv_funcs: Dict[Tuple[int, int], Tuple[str, str, Callable]] = {
    (TempUnit.CELSIUS,TempUnit.KELVIN): ("Celsius", "Kelvin", C_to_kelvin),
    (TempUnit.CELSIUS,TempUnit.FAHRENHEIT): ("Celsius", "Fahrenheit", C_to_Fahrenheit),
    (TempUnit.KELVIN,TempUnit.CELSIUS): ("Kelvin", "Celsius", K_to_celsius),
    (TempUnit.KELVIN,TempUnit.FAHRENHEIT): ("Kelvin", "Fahrenheit", K_to_Fahrenheit),
    (TempUnit.FAHRENHEIT,TempUnit.CELSIUS): ("Fahrenheit", "Celsius", F_to_celsius),
    (TempUnit.FAHRENHEIT,TempUnit.KELVIN): ("Fahrenheit", "Kelvin", F_to_kelvin)
    }


# ============================================================================
# Main Converter Function
# ============================================================================

def angle_converter() -> None:
    """
    Main angle, temperature, weight, and pressure conversion interface.
    Provides interactive menu for conversions.
    """
    while(True):
        try:
            converter_menuMsg()
            op_num = int(input("Enter your choice: "))
            
            if op_num == MenuOptions.QUIT:
                print("\nConverter menu closed\n")
                break
        
            elif op_num == MenuOptions.ANGLE_CONVERSION:
                # Angle conversion
                angle_conversion_menuMsg()
                choice = int(input("Enter your choice: "))

                if choice == AngleUnit.QUIT:
                    continue

                if choice in angle_conv_funcs:
                    name1, func1, name2, func2 = angle_conv_funcs[choice]
                    unit_name = angle_conv_choices[choice-1]
                    print(f"Enter angle in {unit_name}: ", end='')
                    angle = get_val()

                    if angle!=None:
                        ans1, ans2 = convert_angle(name1, func1, name2, func2, angle)
                        print(f"{ans1}\n{ans2}")
                    else:
                        print("No angle given")
                else:
                    print("Invalid choice. select between 1-3")

            elif op_num == MenuOptions.TEMPERATURE_CONVERSION:
                # Temperature conversion
                temp_conv_menuMsg()
                input_choice = int(input("Enter input choice: "))
                output_choice = int(input("Enter output choice: "))

                key = (input_choice, output_choice)

                if key in temp_conv_funcs:
                    print("Enter temperature: ", end='')
                    input_tmp = get_val()

                    if input_tmp is not None:
                        from_tmp, to_tmp, tmp_func = temp_conv_funcs[key]
                        result = tmp_func(input_tmp)
                        print(f"{input_tmp} {from_tmp} = {result} {to_tmp}")
                    else:
                        errmsg()
                else:
                    errmsg()

            elif op_num == MenuOptions.WEIGHT_CONVERSION:
                # Weight conversion with universal converter
                weight_conv_menuMsg()
                input_choice = int(input("\nEnter FROM unit (1-13): "))
                
                # Check for quit
                if input_choice == WeightUnit.QUIT:
                    continue
                
                # Validate input choice
                if input_choice not in WEIGHT_UNIT_NAMES:
                    print("Invalid choice. Please select 1-13.")
                    continue
                
                output_choice = int(input("Enter TO unit (1-13): "))
                
                # Check for quit
                if output_choice == WeightUnit.QUIT:
                    continue
                
                # Validate output choice
                if output_choice not in WEIGHT_UNIT_NAMES:
                    print("Invalid choice. Please select 1-13.")
                    continue
                
                # Check for same unit conversion
                if input_choice == output_choice:
                    print("\n⚠️  Input and output units are the same. No conversion needed.\n")
                    continue

                print("Enter weight: ", end='')
                input_weight = get_val()

                if input_weight is not None:
                    from_unit_name = WEIGHT_UNIT_NAMES[input_choice]
                    to_unit_name = WEIGHT_UNIT_NAMES[output_choice]
                    from_abbrev = WEIGHT_UNIT_ABBREV[input_choice]
                    to_abbrev = WEIGHT_UNIT_ABBREV[output_choice]
                    
                    # Use universal converter
                    result = convert_weight(input_weight, input_choice, output_choice)
                    
                    # Display result
                    print("\n" + "="*50)
                    print(f"   CONVERSION RESULT:")
                    print(f"   {input_weight} {from_abbrev} = {format_result(result)} {to_abbrev}")
                    print(f"   ({from_unit_name} → {to_unit_name})")
                    print("="*50 + "\n")
                else:
                    errmsg()

            elif op_num == MenuOptions.PRESSURE_CONVERSION:
                # Pressure conversion with universal converter
                pressure_conv_menuMsg()
                input_choice = int(input("\nEnter FROM unit (1-6): "))
                
                # Check for quit
                if input_choice == PressureUnit.QUIT:
                    continue
                
                # Validate input choice
                if input_choice not in PRESSURE_UNIT_NAMES:
                    print("Invalid choice. Please select 1-6.")
                    continue
                
                output_choice = int(input("Enter TO unit (1-6): "))
                
                # Check for quit
                if output_choice == PressureUnit.QUIT:
                    continue
                
                # Validate output choice
                if output_choice not in PRESSURE_UNIT_NAMES:
                    print("Invalid choice. Please select 1-6.")
                    continue
                
                # Check for same unit conversion
                if input_choice == output_choice:
                    print("\n⚠️  Input and output units are the same. No conversion needed.\n")
                    continue

                print("Enter pressure: ", end='')
                input_pressure = get_val()

                if input_pressure is not None:
                    from_unit_name = PRESSURE_UNIT_NAMES[input_choice]
                    to_unit_name = PRESSURE_UNIT_NAMES[output_choice]
                    from_abbrev = PRESSURE_UNIT_ABBREV[input_choice]
                    to_abbrev = PRESSURE_UNIT_ABBREV[output_choice]
                    
                    # Use universal converter
                    result = convert_pressure(input_pressure, input_choice, output_choice)
                    
                    # Display result
                    print("\n" + "="*50)
                    print(f"   CONVERSION RESULT:")
                    print(f"   {input_pressure} {from_abbrev} = {format_result(result)} {to_abbrev}")
                    print(f"   ({from_unit_name} → {to_unit_name})")
                    print("="*50 + "\n")
                else:
                    errmsg()

        except (TypeError, UnboundLocalError, SyntaxError, ValueError):
            errmsg()
            continue

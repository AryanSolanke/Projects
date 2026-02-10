"""
Converter Module

Provides angle, temperature, and weight conversion functionality.
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
    """Weight unit types."""
    KILOGRAM = 1
    GRAM = 2
    POUND = 3
    QUIT = 4

class MenuOptions(IntEnum):
    """Conversion unit types."""
    ANGLE_CONVERSION = 1
    TEMPERATURE_CONVERSION = 2
    WEIGHT_CONVERSION = 3
    QUIT = 4

# ============================================================================
# Menu Display Functions
# ============================================================================ 

def converter_menuMsg() -> None:
    """Display main converter menu."""
    print("\n|=====>Convertion Operations<=====|\n")
    print("1. Angle.\n2. Temperature.\n3. Weight.\n4. Quit Converter.")

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
    """Display weight conversion menu."""
    print("\n|=====>Input choices<=====|\n")
    print("Select a input choice\n")
    print("1. Kilogram.\n2. Gram\n3. Pound\n4. Quit Weight Converter.")


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
# Weight Conversion Functions
# ============================================================================

def kg_to_grams(weight: float) -> float:
    """Convert kilograms to grams."""
    return weight * 1000


def grams_to_kg(weight: float) -> float:
    """Convert grams to kilograms."""
    return weight / 1000


def kg_to_pounds(weight: float) -> float:
    """Convert kilograms to pounds.
    
    Conversion: 1 kg = 2.20462 pounds
    """
    return weight * 2.20462


def pounds_to_kg(weight: float) -> float:
    """Convert pounds to kilograms.
    
    Conversion: 1 pound = 0.453592 kg
    """
    return weight * 0.453592


def grams_to_pounds(weight: float) -> float:
    """Convert grams to pounds.
    
    Conversion: 1 gram = 0.00220462 pounds
    """
    return weight * 0.00220462


def pounds_to_grams(weight: float) -> float:
    """Convert pounds to grams.
    
    Conversion: 1 pound = 453.592 grams
    """
    return weight * 453.592


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

# Weight conversion: (from_unit, to_unit, conversion_function)
weight_conv_funcs: Dict[Tuple[int, int], Tuple[str, str, Callable]] = {
    # Kilogram conversions
    (WeightUnit.KILOGRAM, WeightUnit.GRAM): ("Kilogram", "Gram", kg_to_grams),
    (WeightUnit.KILOGRAM, WeightUnit.POUND): ("Kilogram", "Pound", kg_to_pounds),
    
    # Gram conversions
    (WeightUnit.GRAM, WeightUnit.KILOGRAM): ("Gram", "Kilogram", grams_to_kg),
    (WeightUnit.GRAM, WeightUnit.POUND): ("Gram", "Pound", grams_to_pounds),
    
    # Pound conversions
    (WeightUnit.POUND, WeightUnit.KILOGRAM): ("Pound", "Kilogram", pounds_to_kg),
    (WeightUnit.POUND, WeightUnit.GRAM): ("Pound", "Gram", pounds_to_grams),
}


# ============================================================================
# Main Converter Function
# ============================================================================

def angle_converter() -> None:
    """
    Main angle, temperature, and weight conversion interface.
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
                # Weight conversion
                weight_conv_menuMsg()
                input_choice = int(input("Enter input choice: "))
                output_choice = int(input("Enter output choice: "))

                key = (input_choice, output_choice)

                if key in weight_conv_funcs:
                    print("Enter weight: ", end='')
                    input_weight = get_val()

                    if input_weight is not None:
                        from_unit, to_unit, weight_func = weight_conv_funcs[key]
                        result = weight_func(input_weight)
                        print(f"{input_weight} {from_unit} = {result} {to_unit}")
                    else:
                        errmsg()
                else:
                    errmsg()

        except (TypeError, UnboundLocalError, SyntaxError, ValueError):
            errmsg()
            continue

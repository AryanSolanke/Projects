"""
Comprehensive Test Suite for converter.py

This module provides extensive unit tests for the unit converter module,
convering angle and temperature conversions.

Testing Strategy:
1. Conversion accuracy - Verify mathematical correctness
2. Boundary values - Test extreme temperatures and angles
3. Round-trip conversions - Test bidirectional accuracy
4. Type safety - Ensure proper handling of inputs
5. Physical constriants - Verify realistic value handling

Standards:
- pytest framework
- Type hints for all test functions
- Parametrized tests for conversion tables
"""

import pytest
import math
from typing import Tuple
from unittest.mock import patch

# Angle conversion imports
from converter.angle_converter import (
    to_rads, to_deg, to_grad, convert_angle, angle_converter,
    AngleUnit, angle_conv_funcs,
)

# Temperature conversion imports
from converter.temp_converter import (
    C_to_kelvin, C_to_Fahrenheit,
    K_to_celsius, K_to_Fahrenheit,
    F_to_celsius, F_to_kelvin,
    TempUnit, temp_conv_funcs,
)

from std import errmsg


# ============================================================================
# Test Angle Conversion Functions
# ============================================================================

class TestAngleConversion:
    """Test suite for angle conversion functions."""

    # Degree to Radian conversions
    def test_to_rads_standard_angles(self) -> None:
        """
        Test degree to radian conversion for standard angles.
        
        Inputs: 0°, 90°, 180°, 360°
        Expected: 0, π/2, π, 2π radians
        """
        assert abs(to_rads(0) - 0) < 1e-9
        assert abs(to_rads(90) - math.pi/2) < 1e-9
        assert abs(to_rads(180) - math.pi) < 1e-9
        assert abs(to_rads(360) - 2*math.pi) < 1e-9

    def test_to_rads_negative_angles(self) -> None:
        """
        Test radians conversion with negative angles.
        
        Input: -90°
        Expected: -π/2 radians
        """
        assert abs(to_rads(-90) - (-math.pi/2)) < 1e-9

    def test_to_rads_decimal_angles(self) -> None:
        """
        Test radians conversion with decimal degrees.

        Input: 45.5°
        Expected: Correct radian value
        """
        result = to_rads(45.5)
        expected = math.radians(45.5)
        assert abs(result - expected) < 1e-9

    # Radian to Degree conversions
    def test_to_deg_standard_radians(self) -> None:
        """
        Test radians to Degree conversion.

        Inputs: 0, π/2, π, 2π
        Expected: 0°, 90°, 180°, 360°
        """
        assert abs(to_deg(0) - 0) < 1e-9
        assert abs(to_deg(math.pi/2) - 90) < 1e-9
        assert abs(to_deg(math.pi) - 180) < 1e-9
        assert abs(to_deg(2*math.pi) - 360) < 1e-9

    def test_to_deg_negative_radians(self) -> None:
        """
        Test degree conversion with negavtive radians.

        Input: -π
        Expected: -180°
        """
        assert abs(to_deg(-math.pi) - (-180)) < 1e-9

    # Degree to Gradian conversions
    def test_to_grad_standard_angles(self) -> None:
        """
        Test degree to gradian conversion.

        Inputs: 0°, 90°, 180°, 360°
        Expected: 0, 100, 200, 400 gradians
        """
        assert abs(to_grad(0) - 0) < 1e-9
        assert abs(to_grad(90) - 100) < 1e-9
        assert abs(to_grad(180) - 200) < 1e-9
        assert abs(to_grad(360) - 400) < 1e-9

    def test_to_grad_formula(self) -> None:
        """
        Verify gradian formula: grad = deg * 200/180.

        Input: 45°
        Expected: 50 gradians
        """
        assert abs(to_grad(45) - 50) < 1e-9

    # Round-trip conversion tests
    def test_deg_rad_deg_roundtrip(self) -> None:
        """
        Test degree → radian → degree round-trip.
        
        Input: 45°
        Expected: Back to 45° after conversions
        """
        original = 45
        rad = to_rads(original)
        back = to_deg(rad)
        assert (back - original) < 1e-9

    def test_deg_grad_consistency(self) -> None:
        """
        Test that degree and gradian conversions are consistent.
        
        Property: 90° = 100 grad
        """
        deg_value = 90
        grad_value = to_grad(deg_value)
        expected = 100
        assert abs(grad_value - expected) < 1e-9

    @pytest.mark.parametrize("degrees,radians", [
        (0, 0),
        (30, math.pi/6),
        (45, math.pi/4),
        (60, math.pi/3),
        (90, math.pi/2),
        (180, math.pi),
        (270, 3*math.pi/2),
        (360, 2*math.pi),
    ])
    def test_degree_radian_parametrized(
        self, degrees: float, radians: float
    ) -> None:
        """Parametrized test for degree-radian conversions."""
        assert abs(to_rads(degrees) - radians) < 1e-9


# ============================================================================
# Test Temperature Conversion Functions
# ============================================================================

class TestTemperatureConversions:
    """Test suite for temperature comversion functions."""

    # Celsius conversions
    def test_C_to_kelvin_standard(self) -> None:
        """
        Test celsius to kelvin conversion.
        
        Inputs: 0°C, 100°C, -273.15°C
        Expected: 273.15K, 373.15K, 0K
        """
        assert abs(C_to_kelvin(0) - 273.15) < 1e-9
        assert abs(C_to_kelvin(100) - 373.15) < 1e-9
        assert abs(C_to_kelvin(-273.15) - 0) < 1e-9

    def test_C_to_Fahrenheit_standard(self) -> None:
        """
        Test celsius to Fahrenheit conversion.
        
        Inputs: 0°C, 100°C, -40°C
        Expected: 32°F, 212°F, -40°F
        """
        assert abs(C_to_Fahrenheit(0) - 32) < 1e-9
        assert abs(C_to_Fahrenheit(100) - 212) < 1e-9
        assert abs(C_to_Fahrenheit(-40) - (-40)) < 1e-9

    def test_C_to_Fahrenheit_formua(self) -> None:
        """
        Verify Fahrenheit formula: F = (9/5)C + 32.
        
        Input: 25°C
        Expected: 77°F
        """
        result = C_to_Fahrenheit(25)
        expected = 77
        assert abs(result - expected) < 1e-9

    # Kelvin conversions
    def test_K_to_celsius_standard(self) -> None:
        """
        Test Kelvin to Celsius conversion.
        
        Inputs: 273.15K, 373.15K, 0K
        Expected: 0°C, 100°C, -273.15°C
        """
        assert abs(K_to_celsius(273.15) - 0) < 1e-9
        assert abs(K_to_celsius(373.15) - 100) < 1e-9
        assert abs(K_to_celsius(0) - (-273.15)) < 1e-9
    
    def test_K_to_Fahrenheit_standard(self) -> None:
        """
        Test Kelvin to Fahrenheit conversion.
        
        Input: 273.15K
        Expected: 32°F (freezing point)
        """
        result = K_to_Fahrenheit(273.15)
        expected = 32
        assert abs(result - expected) < 1e-6

    # Fahrenheit conversions
    def test_F_to_celsius_standard(self) -> None:
        """
        Test Fahrenheit to Celsius conversion.
        
        Inputs: 32°F, 212°F, -40°F
        Expected: 0°C, 100°C, -40°C
        """
        assert abs(F_to_celsius(32) - 0) < 1e-9
        assert abs(F_to_celsius(212) - 100) < 1e-9
        assert abs(F_to_celsius(-40) - (-40)) < 1e-9
    
    def test_F_to_kelvin_standard(self) -> None:
        """
        Test Fahrenheit to Kelvin conversion.
        
        Input: 32°F
        Expected: 273.15K
        """
        result = F_to_kelvin(32)
        expected = 273.15
        assert abs(result - expected) < 1e-9

    # Round-trip conversions
    def test_celsius_kelvin_celsius_roundtrip(self) -> None:
        """
        Test Celsius → Kelvin → Celsius round-trip.
        
        Input: 25°C
        Expected: Back to 25°C
        """
        original = 25
        kelvin = C_to_kelvin(original)
        back = K_to_celsius(kelvin)
        assert abs(back - original) < 1e-9
    
    def test_celsius_fahrenheit_celsius_roundtrip(self) -> None:
        """
        Test Celsius → Fahrenheit → Celsius round-trip.
        
        Input: 30°C
        Expected: Back to 30°C
        """
        original = 30
        fahrenheit = C_to_Fahrenheit(original)
        back = F_to_celsius(fahrenheit)
        assert abs(back - original) < 1e-9
    
    def test_fahrenheit_kelvin_fahrenheit_roundtrip(self) -> None:
        """
        Test Fahrenheit → Kelvin → Fahrenheit round-trip.
        
        Input: 68°F
        Expected: Back to 68°F
        """
        original = 68
        kelvin = F_to_kelvin(original)
        celsius = K_to_celsius(kelvin)
        back = C_to_Fahrenheit(celsius)
        assert abs(back - original) < 1e-9

    # Physical constriants
    def test_absolute_zero_conversions(self) -> None:
        """
        Test conversions at absolute zero.
        
        0K = -273.15°C = -459.67°F
        """
        abs_zero_C = -273.15
        abs_zero_K = C_to_kelvin(abs_zero_C)
        assert abs(abs_zero_K - 0) < 1e-9
        
        abs_zero_F = C_to_Fahrenheit(abs_zero_C)
        assert abs(abs_zero_F - (-459.67)) < 0.01
    
    def test_water_freezing_point_all_scales(self) -> None:
        """
        Test water freezing point in all scales.
        
        0°C = 273.15K = 32°F
        """
        celsius = 0
        kelvin = C_to_kelvin(celsius)
        fahrenheit = C_to_Fahrenheit(celsius)
        
        assert abs(kelvin - 273.15) < 1e-9
        assert abs(fahrenheit - 32) < 1e-9
    
    def test_water_boiling_point_all_scales(self) -> None:
        """
        Test water boiling point in all scales.
        
        100°C = 373.15K = 212°F
        """
        celsius = 100
        kelvin = C_to_kelvin(celsius)
        fahrenheit = C_to_Fahrenheit(celsius)
        
        assert abs(kelvin - 373.15) < 1e-9
        assert abs(fahrenheit - 212) < 1e-9

    @pytest.mark.parametrize("celsius, kelvin, fahrenheit", [
        (0, 273.15, 32),
        (100, 373.15, 212),
        (-40, 233.15, -40),
        (25, 298.15, 77),
        (-273.15, 0, -459.67),
    ])
    def test_temp_triple_parametrized(
        self, celsius: float, kelvin: float, fahrenheit: float
    ) -> None:
        """
        Parametrized test for temperature conversions.

        Tests C→K, C→F for known temperature points.
        """
        assert abs(C_to_kelvin(celsius) - kelvin) < 1e-6
        assert abs(C_to_Fahrenheit(celsius) - fahrenheit) < 0.01


# ============================================================================
# Test convert_angle Function
# ============================================================================

class TestConvertAngleFunction:
    """Test suite for the convert_angle helper function."""

    def test_convert_angle_returns_two_results(self) -> None:
        """
        Test that convert_angle returns two conversion results.
        
        Input: 90 degrees
        Expected: Tuple of 2 strings
        """
        result = convert_angle("rad", to_rads, "grad", to_grad, 90)
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_convert_angle_format(self) -> None:
        """
        Test that convert_angle formats results correctly.
        
        Input: 180 degrees
        Expected: Strings containing function names and results
        """
        ans1, ans2 = convert_angle("rad", to_rads, "grad", to_grad, 180)
        assert "rad(180)" in ans1
        assert "grad(180)" in ans2
    
    def test_convert_angle_accuracy(self) -> None:
        """
        Test conversion accuracy through convert_angle.
        
        Input: 45 degrees
        Expected: Correct radian and gradian values
        """
        ans1, ans2 = convert_angle("rad", to_rads, "grad", to_grad, 45)
        # Should contain π/4 for radians and 50 for gradians
        assert "0.785398" in ans1 or "0.78539" in ans1  # π/4 ≈ 0.785398
        assert "50" in ans2


# ============================================================================
# Test Lookup Tables
# ============================================================================

class TestLookupTables:
    """Test suite for conversion lookup tables."""

    def test_angle_conv_funcs_completness(self) -> None:
        """
        Test that angle_conv_funcs has all required entries.
        
        Expected: Keys 1, 2, 3 present
        """
        assert AngleUnit.DEGREE in angle_conv_funcs
        assert AngleUnit.RADIAN in angle_conv_funcs
        assert AngleUnit.GRADIAN in angle_conv_funcs

    def test_angle_conv_funcs_structure(self) -> None:
        """
        Test that angle_conv_funcs entries have correct structure.
        
        Expected: Each entry is (str, func, str, func)
        """
        for key, value in angle_conv_funcs.items():
            assert isinstance(value, tuple)
            assert len(value) == 4
            assert isinstance(value[0], str) # name1
            assert callable(value[1])      # func1
            assert isinstance(value[2], str) # name2
            assert callable(value[3])      # func2

    def test_temp_conv_funcs_completeness(self) -> None:
        """
        Test that temp_conv_funcs has all conversion pairs.
        
        Expected: All 6 conversion pairs present
        """
        expected_keys = [
            (TempUnit.CELSIUS, TempUnit.KELVIN),
            (TempUnit.CELSIUS, TempUnit.FAHRENHEIT),
            (TempUnit.KELVIN, TempUnit.CELSIUS),
            (TempUnit.KELVIN, TempUnit.FAHRENHEIT),
            (TempUnit.FAHRENHEIT, TempUnit.CELSIUS),
            (TempUnit.FAHRENHEIT, TempUnit.KELVIN),
        ]
        for key in expected_keys:
            assert key in temp_conv_funcs

    def test_temp_conv_funcs_structure(self) -> None:
        """
        Test that temp_conv_funcs entries have correct structure.
        
        Expected: Each entry is (str, str, func)
        """
        for key, value in temp_conv_funcs.items():
            assert isinstance(value, tuple)
            assert len(value) == 3
            assert isinstance(value[0], str)  # from_unit
            assert isinstance(value[1], str)  # to_unit
            assert callable(value[2])         # conversion_func


# ============================================================================
# Test Edge Cases
# ============================================================================

class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_zero_angle_conversions(self) -> None:
        """
        Test conversions with zero angle.
        
        Input: 0
        Expected: 0 in all units
        """
        assert to_rads(0) == 0
        assert to_deg(0) == 0
        assert to_grad(0) == 0

    def test_negative_angle_conversions(self) -> None:
        """
        Test conversions with negative angles.
        
        Input: -90 degrees
        Expected: Correct negative values
        """
        assert to_rads(-90) < 0
        assert to_grad(-90) < 0

    def test_large_angle_conversions(self) -> None:
        """
        Test conversions with very large angles.
        
        Input: 3600 degrees (10 full rotations)
        Expected: Valid results
        """
        result = to_rads(3600)
        expected = 20 * math.pi
        assert abs(result - expected) < 1e-6

    def test_very_small_angle_conversions(self) -> None:
        """
        Test conversions with very small angles.
        
        Input: 0.001 degrees
        Expected: Valid small radian value
        """
        result = to_rads(0.001)
        assert result > 0
        assert result < 0.001  # Should be even smaller in radians

    def test_negative_kelvin_handling(self) -> None:
        """
        Test conversion from impossible negative Kelvin.
        
        Note: This tests mathematical conversion, not physical validity.
        Input: -10K
        Expected: Mathematical result (would be below absolute zero)
        """
        result = K_to_celsius(-10)
        assert result < -273.15  # Below absolute zero (unphysical but mathematically correct)

    def test_extreme_temperature_celsius(self) -> None:
        """
        Test conversions with extreme temperatures.
        
        Input: 1000°C
        Expected: 1273.15K, 1832°F
        """
        kelvin = C_to_kelvin(1000)
        fahrenheit = C_to_Fahrenheit(1000)
        assert abs(kelvin - 1273.15) < 1e-9
        assert abs(fahrenheit - 1832) < 1e-9


# ============================================================================
# Test Physical Constants and Known Values
# ============================================================================

class TestPhysicalConstants:
    """Test conversions at known physical constants."""
    
    def test_right_angle_conversions(self) -> None:
        """
        Test right angle in all units.
        
        90° = π/2 rad = 100 grad
        """
        degrees = 90
        radians = to_rads(degrees)
        gradians = to_grad(degrees)
        
        assert abs(radians - math.pi/2) < 1e-9
        assert abs(gradians - 100) < 1e-9
    
    def test_straight_angle_conversions(self) -> None:
        """
        Test straight angle in all units.
        
        180° = π rad = 200 grad
        """
        degrees = 180
        radians = to_rads(degrees)
        gradians = to_grad(degrees)
        
        assert abs(radians - math.pi) < 1e-9
        assert abs(gradians - 200) < 1e-9
    
    def test_body_temperature_conversions(self) -> None:
        """
        Test normal human body temperature.
        
        37°C = 310.15K = 98.6°F
        """
        celsius = 37
        kelvin = C_to_kelvin(celsius)
        fahrenheit = C_to_Fahrenheit(celsius)
        
        assert abs(kelvin - 310.15) < 1e-9
        assert abs(fahrenheit - 98.6) < 0.1
    
    def test_room_temperature_conversions(self) -> None:
        """
        Test standard room temperature.
        
        20°C = 293.15K = 68°F
        """
        celsius = 20
        kelvin = C_to_kelvin(celsius)
        fahrenheit = C_to_Fahrenheit(celsius)
        
        assert abs(kelvin - 293.15) < 1e-9
        assert abs(fahrenheit - 68) < 1


# ============================================================================
# Test Precision and Accuracy
# ============================================================================

class TestPrecisionAccuracy:
    """Test numerical precision and accuracy of conversions."""
    
    def test_high_precision_angle_conversion(self) -> None:
        """
        Test that angle conversions maintain high precision.
        
        Input: π radians
        Expected: Exactly 180 degrees
        """
        radians = math.pi
        degrees = to_deg(radians)
        assert abs(degrees - 180) < 1e-10
    
    def test_high_precision_temperature_conversion(self) -> None:
        """
        Test that temperature conversions maintain precision.
        
        Input: 0°C
        Expected: Exactly 273.15K
        """
        celsius = 0
        kelvin = C_to_kelvin(celsius)
        assert abs(kelvin - 273.15) < 1e-12
    
    def test_multiple_conversion_precision_loss(self) -> None:
        """
        Test precision loss through multiple conversions.
        
        Action: C→K→C→F→C
        Expected: Minimal precision loss
        """
        original = 25.123456789
        k = C_to_kelvin(original)
        c1 = K_to_celsius(k)
        f = C_to_Fahrenheit(c1)
        c2 = F_to_celsius(f)
        
        assert abs(c2 - original) < 1e-9


class TestConverterErrorMessages:
    """Test suite for error messages in converter module."""

    def test_invalid_angle_choice_message(self, capsys, monkeypatch) -> None:
        """Test error message for invalid angle unit choice.
        
        Scenario: User enters invalid choice (99) for angle unit selection
        Expected: "❌ Invalid choice. Please select 1-3"
        """
        # Simulate user input: invalid choice 99, then quit with 4
        inputs = iter(['99', '4'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        # Run converter
        angle_converter()

        # Capture output
        captured = capsys.readouterr()

        # Verify exact error message
        assert "❌ Invalid choice. Please select 1-3" in captured.out

    def test_no_angle_given_error_message(self, capsys, monkeypatch) -> None:
        """
        Test error message when no angle value is entered.

        Expected: "⚠️  No angle given"
        """
        with patch('sci.get_val', return_value=None):
            inputs = iter(['1', '4'])  # 1 = degree, 4 = quit
            monkeypatch.setattr('builtins.input', lambda _: next(inputs))

            angle_converter()

            captured = capsys.readouterr()
            assert "⚠️  No angle given" in captured.out
    
    def test_converter_menu_closed_message(self, capsys, monkeypatch) -> None:
        """
        Test that angle_converter closes properly.
        
        Expected: Menu displays, then converter returns (no specific message)
        """
        inputs = iter(['4'])  # 4 = Quit Angle Converter
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        angle_converter()

        captured = capsys.readouterr()
        assert "ANGLE CONVERSION" in captured.out

    def test_error_invalid_input_from_message(self, capsys) -> None:
        """
        Test generic error message from errmsg() function.

        Expected: "❌ Error: Invalid input."
        """
        errmsg()
        captured = capsys.readouterr()
        assert captured.out.strip() == "❌ Error: Invalid input."


class TestConverterInvalidInputs:
    """Test suite for invalid input handling in converter functions."""

    def test_to_rads_with_non_numeric_string_raises_error(self) -> None:
        """
        Test to_rads with non numeric string input.

        Input: "abc"
        Expected: TypeError or ValueError
        """
        with pytest.raises((TypeError, ValueError)):
            to_rads("abc")
    
    def test_to_deg_with_non_numeric_string_raises_error(self) -> None:
        """
        Test to_deg with non-numeric string input.
        
        Input: "xyz"
        Expected: TypeError or ValueError
        """
        with pytest.raises((TypeError, ValueError)):
            to_deg("xyz")
    
    def test_to_grad_with_non_numeric_string_raises_error(self) -> None:
        """
        Test to_grad with non-numeric string input.
        
        Input: "invalid"
        Expected: TypeError or ValueError
        """
        with pytest.raises((TypeError, ValueError)):
            to_grad("invalid")

    def test_to_rads_with_none_raises_error(self) -> None:
        """
        Test to_rads with None input.
        
        Input: None
        Expected: TypeError
        """
        with pytest.raises(TypeError):
            to_rads(None)
    
    def test_C_to_kelvin_with_string_raises_error(self) -> None:
        """
        Test C_to_kelvin with string input.
        
        Input: "25 degrees"
        Expected: TypeError
        """
        with pytest.raises(TypeError):
            C_to_kelvin("25 degrees")
    
    def test_F_to_celsius_with_none_raises_error(self) -> None:
        """
        Test F_to_celsius with None input.
        
        Input: None
        Expected: TypeError
        """
        with pytest.raises(TypeError):
            F_to_celsius(None)


class TestConverterLookupTableValidation:
    """Test lookup table validation for error handling."""

    def test_angle_conv_funcs_rejects_invalid_keys(self) -> None:
        """
        Test that invalid angle unit choices are not in the lookup table.

        Invalid keys: 0, 4, 5, -1, etc.
        """
        invalid_keys = [0, 4, 5, -1, 100]

        for key in invalid_keys:
            assert key not in angle_conv_funcs, \
                f"Invalid key {key} should not be in angle_conv_funcs"
            
            # Attempting to access should raise KeyError
            with pytest.raises(KeyError):
                _ = angle_conv_funcs[key]

    def test_temp_conv_funcs_rejects_same_unit_pairs(self) -> None:
        """
        Test that same-unit temperature pairs are not in lookup table.
        
        Invalid pairs: (C,C), (K,K), (F,F)
        """
        invalid_keys = [
            (TempUnit.CELSIUS, TempUnit.CELSIUS),
            (TempUnit.KELVIN, TempUnit.KELVIN),
            (TempUnit.FAHRENHEIT, TempUnit.FAHRENHEIT),
        ]
        
        for key in invalid_keys:
            assert key not in temp_conv_funcs, \
                f"Same-unit pair {key} should not be in temp_conv_funcs"
    
    def test_temp_conv_funcs_rejects_invalid_unit_numbers(self) -> None:
        """
        Test that invalid temperature unit numbers are not in lookup table.
        
        Invalid: (0,1), (99,1), etc.
        """
        invalid_keys = [(0, 1), (1, 0), (99, 1), (1, 99)]
        
        for key in invalid_keys:
            assert key not in temp_conv_funcs


class TestConverterEdgeCaseErrors:
    """Test edge case error scenarios in converter."""

    def test_angle_conversion_with_infinity(self) -> None:
        """
        Test angle conversion with infinity.

        Input: float('inf)
        Expected: Result is infinity
        """
        result_rad = to_rads(float('inf'))
        result_grad = to_grad(float('inf'))

        assert math.isinf(result_rad)
        assert math.isinf(result_grad)

    def test_angle_conversion_with_negative_infinity(self) -> None:
        """
        Test angle conversion with negative infinity.

        Input: float('inf')
        Expected: Result is negative infinity
        """
        result_rad = to_rads(float('-inf'))
        
        assert math.isinf(result_rad)
        assert result_rad < 0

    def test_angle_conversion_with_nan(self) -> None:
        """
        Test angle conversion with NaN.
        
        Input: float('nan')
        Expected: Result is NaN
        """
        result_rad = to_rads(float('nan'))
        result_grad = to_grad(float('nan'))
        
        assert math.isnan(result_rad)
        assert math.isnan(result_grad)
    
    def test_temperature_conversion_with_infinity(self) -> None:
        """
        Test temperature conversion with infinity.
        
        Input: float('inf')
        Expected: Result is infinity
        """
        result_k = C_to_kelvin(float('inf'))
        result_f = C_to_Fahrenheit(float('inf'))
        
        assert math.isinf(result_k)
        assert math.isinf(result_f)
    
    def test_temperature_conversion_with_nan(self) -> None:
        """
        Test temperature conversion with NaN.
        
        Input: float('nan')
        Expected: Result is NaN
        """
        result_k = C_to_kelvin(float('nan'))
        
        assert math.isnan(result_k)
    
    def test_temperature_below_absolute_zero(self) -> None:
        """
        Test temperature conversion below absolute zero.
        
        Input: -300°C (below -273.15°C)
        Expected: Mathematically computed (negative Kelvin - unphysical)
        """
        result_k = C_to_kelvin(-300)
        
        assert isinstance(result_k, float)
        assert result_k < 0  # Unphysical but mathematically computed


class TestConverterErrorMessageFormats:
    """Test that error messages follow expected format and content."""
    
    def test_invalid_choice_message_format(self, capsys, monkeypatch) -> None:
        """
        Test exact format of invalid choice message.
        
        Expected: "❌ Invalid choice. Please select 1-3"
        """
        inputs = iter(['999', '4'])  # 999=invalid choice, 4=quit
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        
        angle_converter()
        
        captured = capsys.readouterr()
        assert "❌ Invalid choice" in captured.out
        assert "1-3" in captured.out
    
    def test_no_angle_given_message_format(self, capsys, monkeypatch) -> None:
        """
        Test exact format of "no angle given" message.
        
        Expected: "⚠️  No angle given"
        """
        with patch('sci.get_val', return_value=None):
            inputs = iter(['1', '4'])  # 1 = degree, 4 = quit
            monkeypatch.setattr('builtins.input', lambda _: next(inputs))
            
            angle_converter()
            
            captured = capsys.readouterr()
            assert "⚠️  No angle given" in captured.out
    
    def test_error_message_from_std_module(self, capsys) -> None:
        """
        Test that errmsg() from std module produces expected format.
        
        Expected: "❌ Error: Invalid input." with period
        """
        errmsg()
        captured = capsys.readouterr()
        
        assert captured.out.strip() == "❌ Error: Invalid input."


class TestConverterBoundaryErrors:
    """Test error handling at mathematical and physical boundaries."""
    
    def test_temperature_at_absolute_zero_no_error(self) -> None:
        """
        Test that absolute zero doesn't produce errors.
        
        Input: -273.15°C
        Expected: Valid conversion to 0 K
        """
        result = C_to_kelvin(-273.15)
        assert abs(result - 0) < 1e-12
    
    def test_very_large_positive_angle_no_overflow_error(self) -> None:
        """
        Test that very large angles don't cause overflow errors.
        
        Input: 10^100 degrees
        Expected: Computes without error
        """
        large_angle = 10**100
        result_rad = to_rads(large_angle)
        
        assert isinstance(result_rad, float)
    
    def test_very_small_positive_angle_no_underflow_error(self) -> None:
        """
        Test that very small angles don't cause underflow errors.
        
        Input: 10^-100 degrees
        Expected: Computes correctly
        """
        small_angle = 10**-100
        result_rad = to_rads(small_angle)
        
        assert isinstance(result_rad, float)
    
    def test_temperature_conversion_at_water_freezing_no_error(self) -> None:
        """
        Test conversion at water freezing point.
        
        Input: 0°C
        Expected: Exact conversions without errors
        """
        k_freeze = C_to_kelvin(0)
        f_freeze = C_to_Fahrenheit(0)
        
        assert abs(k_freeze - 273.15) < 1e-12
        assert abs(f_freeze - 32) < 1e-12
    
    def test_temperature_conversion_at_water_boiling_no_error(self) -> None:
        """
        Test conversion at water boiling point.
        
        Input: 100°C
        Expected: Exact conversions without errors
        """
        k_boil = C_to_kelvin(100)
        f_boil = C_to_Fahrenheit(100)
        
        assert abs(k_boil - 373.15) < 1e-12
        assert abs(f_boil - 212) < 1e-12


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

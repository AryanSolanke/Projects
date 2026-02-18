"""
Angle Converter Test Suite

Tests for angle conversion functions: degrees, radians, gradians.

Coverage:
- Conversion functions: to_rads(), to_deg(), to_grad(), convert_angle()
- Lookup table: angle_conv_funcs
- Edge cases, precision, boundary errors
- UI: angle_converter() error messages
"""

import pytest
from decimal import Decimal
import math
from unittest.mock import patch

from converter.angle_converter import (
    to_rads as _to_rads,
    to_deg as _to_deg,
    to_grad as _to_grad,
    convert_angle,
    angle_converter,
    AngleUnit, angle_conv_funcs,
)

def _to_float(value):
    return float(value) if isinstance(value, Decimal) else value


def to_rads(value):
    return _to_float(_to_rads(value))


def to_deg(value):
    return _to_float(_to_deg(value))


def to_grad(value):
    return _to_float(_to_grad(value))
from std import errmsg


# ============================================================================
# Conversion Functions
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
        Test degree conversion with negative radians.

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
        assert "0.785398" in ans1 or "0.78539" in ans1  # π/4 ≈ 0.785398
        assert "50" in ans2


# ============================================================================
# Lookup Tables
# ============================================================================

class TestAngleLookupTables:
    """Test suite for angle conversion lookup tables."""

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
            assert isinstance(value[0], str)
            assert callable(value[1])
            assert isinstance(value[2], str)
            assert callable(value[3])

    def test_angle_conv_funcs_rejects_invalid_keys(self) -> None:
        """
        Test that invalid angle unit choices are not in the lookup table.

        Invalid keys: 0, 4, 5, -1, etc.
        """
        invalid_keys = [0, 4, 5, -1, 100]

        for key in invalid_keys:
            assert key not in angle_conv_funcs, \
                f"Invalid key {key} should not be in angle_conv_funcs"
            with pytest.raises(KeyError):
                _ = angle_conv_funcs[key]


# ============================================================================
# Edge Cases, Physical Constants, Precision
# ============================================================================

class TestAngleEdgeCases:
    """Test edge cases and boundary conditions for angle conversions."""

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
        assert result < 0.001

    def test_angle_conversion_with_infinity(self) -> None:
        """
        Test angle conversion with infinity.

        Input: float('inf')
        Expected: Result is infinity
        """
        result_rad = to_rads(float('inf'))
        result_grad = to_grad(float('inf'))
        assert math.isinf(result_rad)
        assert math.isinf(result_grad)

    def test_angle_conversion_with_negative_infinity(self) -> None:
        """
        Test angle conversion with negative infinity.

        Input: float('-inf')
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


class TestAnglePhysicalConstants:
    """Test angle conversions at known physical constants."""

    def test_right_angle_conversions(self) -> None:
        """
        Test right angle in all units.
        
        90° = π/2 rad = 100 grad
        """
        degrees = 90
        assert abs(to_rads(degrees) - math.pi/2) < 1e-9
        assert abs(to_grad(degrees) - 100) < 1e-9

    def test_straight_angle_conversions(self) -> None:
        """
        Test straight angle in all units.
        
        180° = π rad = 200 grad
        """
        degrees = 180
        assert abs(to_rads(degrees) - math.pi) < 1e-9
        assert abs(to_grad(degrees) - 200) < 1e-9


class TestAnglePrecision:
    """Test numerical precision and accuracy of angle conversions."""

    def test_high_precision_angle_conversion(self) -> None:
        """
        Test that angle conversions maintain high precision.
        
        Input: π radians
        Expected: Exactly 180 degrees
        """
        degrees = to_deg(math.pi)
        assert abs(degrees - 180) < 1e-10

    def test_very_large_positive_angle_no_overflow_error(self) -> None:
        """
        Test that very large angles don't cause overflow errors.
        
        Input: 10^100 degrees
        Expected: Computes without error
        """
        result_rad = to_rads(10**100)
        assert isinstance(result_rad, float)

    def test_very_small_positive_angle_no_underflow_error(self) -> None:
        """
        Test that very small angles don't cause underflow errors.
        
        Input: 10^-100 degrees
        Expected: Computes correctly
        """
        result_rad = to_rads(10**-100)
        assert isinstance(result_rad, float)


# ============================================================================
# Invalid Inputs
# ============================================================================

class TestAngleInvalidInputs:
    """Test invalid input handling for angle conversion functions."""

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


# ============================================================================
# UI / angle_converter() Tests
# ============================================================================

class TestAngleConverterUI:
    """Test angle_converter() user-facing messages and behaviour."""

    def test_invalid_angle_choice_message(self, capsys, monkeypatch) -> None:
        """
        Test error message for invalid angle unit choice.
        
        Scenario: User enters invalid choice (99) for angle conversion
        Expected: "Invalid choice. Please select 1-3"
        """
        inputs = iter(['99', '4'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        angle_converter()
        captured = capsys.readouterr()
        assert "Invalid choice. Please select 1-3" in captured.out

    def test_no_angle_given_error_message(self, capsys, monkeypatch) -> None:
        """
        Test error message when no angle value is entered.

        Expected: "No angle given"
        """
        with patch('sci.get_val', return_value=None):
            inputs = iter(['1', '4'])
            monkeypatch.setattr('builtins.input', lambda _: next(inputs))
            angle_converter()
            captured = capsys.readouterr()
            assert "No angle given" in captured.out

    def test_converter_menu_closed_message(self, capsys, monkeypatch) -> None:
        """
        Test angle_converter displays menu then returns silently on quit.
        """
        inputs = iter(['4'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        angle_converter()
        captured = capsys.readouterr()
        assert "ANGLE CONVERSION" in captured.out

    def test_error_invalid_input_from_errmsg(self, capsys) -> None:
        """
        Test generic error message from errmsg() function.

        Expected: "Error: Invalid input."
        """
        errmsg()
        captured = capsys.readouterr()
        assert captured.out.strip() == "Error: Invalid input."

    def test_invalid_choice_message_format(self, capsys, monkeypatch) -> None:
        """
        Test exact format of invalid choice message.
        
        Expected: "Invalid choice. Please select 1-3"
        """
        inputs = iter(['999', '4'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        angle_converter()
        captured = capsys.readouterr()
        assert "Invalid choice" in captured.out
        assert "1-3" in captured.out

    def test_no_angle_given_message_format(self, capsys, monkeypatch) -> None:
        """
        Test exact format of "no angle given" message.
        
        Expected: "No angle given"
        """
        with patch('sci.get_val', return_value=None):
            inputs = iter(['1', '4'])
            monkeypatch.setattr('builtins.input', lambda _: next(inputs))
            angle_converter()
            captured = capsys.readouterr()
            assert "No angle given" in captured.out

    def test_error_message_from_std_module(self, capsys) -> None:
        """
        Test that errmsg() produces expected format.
        
        Expected: "Error: Invalid input." with period
        """
        errmsg()
        captured = capsys.readouterr()
        assert captured.out.strip() == "Error: Invalid input."


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

"""
Temperature Converter Test Suite

Tests for temperature conversion functions: Celsius, Kelvin, Fahrenheit.

Coverage:
- Conversion functions: C_to_kelvin, C_to_Fahrenheit, K_to_celsius,
  K_to_Fahrenheit, F_to_celsius, F_to_kelvin
- Lookup table: temp_conv_funcs
- Physical constants, round-trips, edge cases, precision, boundary errors
"""

import pytest
from decimal import Decimal

from calculator.converters.temperature import (
    C_to_kelvin,
    C_to_Fahrenheit,
    K_to_celsius,
    K_to_Fahrenheit,
    F_to_celsius,
    F_to_kelvin,
    TempUnit, temp_conv_funcs,
)

def _dec(value: Decimal | int | str) -> Decimal:
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))

def _assert_close(actual: Decimal, expected: Decimal | int | str, tol: Decimal | int | str = "1e-9") -> None:
    assert abs(actual - _dec(expected)) < _dec(tol)

# ============================================================================
# Conversion Functions
# ============================================================================

class TestTemperatureConversions:
    """Test suite for temperature conversion functions."""

    # Celsius conversions
    def test_C_to_kelvin_standard(self) -> None:
        """
        Test celsius to kelvin conversion.
        
        Inputs: 0°C, 100°C, -273.15°C
        Expected: 273.15K, 373.15K, 0K
        """
        _assert_close(C_to_kelvin(0), "273.15")
        _assert_close(C_to_kelvin(100), "373.15")
        _assert_close(C_to_kelvin(Decimal("-273.15")), 0)

    def test_C_to_Fahrenheit_standard(self) -> None:
        """
        Test celsius to Fahrenheit conversion.
        
        Inputs: 0°C, 100°C, -40°C
        Expected: 32°F, 212°F, -40°F
        """
        _assert_close(C_to_Fahrenheit(0), 32)
        _assert_close(C_to_Fahrenheit(100), 212)
        _assert_close(C_to_Fahrenheit(-40), -40)

    def test_C_to_Fahrenheit_formula(self) -> None:
        """
        Verify Fahrenheit formula: F = (9/5)C + 32.
        
        Input: 25°C
        Expected: 77°F
        """
        _assert_close(C_to_Fahrenheit(25), 77)

    # Kelvin conversions
    def test_K_to_celsius_standard(self) -> None:
        """
        Test Kelvin to Celsius conversion.
        
        Inputs: 273.15K, 373.15K, 0K
        Expected: 0°C, 100°C, -273.15°C
        """
        _assert_close(K_to_celsius(Decimal("273.15")), 0)
        _assert_close(K_to_celsius(Decimal("373.15")), 100)
        _assert_close(K_to_celsius(0), "-273.15")

    def test_K_to_Fahrenheit_standard(self) -> None:
        """
        Test Kelvin to Fahrenheit conversion.
        
        Input: 273.15K
        Expected: 32°F (freezing point)
        """
        _assert_close(K_to_Fahrenheit(Decimal("273.15")), 32, "1e-6")

    # Fahrenheit conversions
    def test_F_to_celsius_standard(self) -> None:
        """
        Test Fahrenheit to Celsius conversion.
        
        Inputs: 32°F, 212°F, -40°F
        Expected: 0°C, 100°C, -40°C
        """
        _assert_close(F_to_celsius(32), 0)
        _assert_close(F_to_celsius(212), 100)
        _assert_close(F_to_celsius(-40), -40)

    def test_F_to_kelvin_standard(self) -> None:
        """
        Test Fahrenheit to Kelvin conversion.
        
        Input: 32°F
        Expected: 273.15K
        """
        _assert_close(F_to_kelvin(32), "273.15")

    # Round-trip conversions
    def test_celsius_kelvin_celsius_roundtrip(self) -> None:
        """
        Test Celsius → Kelvin → Celsius round-trip.
        
        Input: 25°C
        Expected: Back to 25°C
        """
        original = 25
        back = K_to_celsius(C_to_kelvin(original))
        _assert_close(back, original)

    def test_celsius_fahrenheit_celsius_roundtrip(self) -> None:
        """
        Test Celsius → Fahrenheit → Celsius round-trip.
        
        Input: 30°C
        Expected: Back to 30°C
        """
        original = 30
        back = F_to_celsius(C_to_Fahrenheit(original))
        _assert_close(back, original)

    def test_fahrenheit_kelvin_fahrenheit_roundtrip(self) -> None:
        """
        Test Fahrenheit → Kelvin → Fahrenheit round-trip.
        
        Input: 68°F
        Expected: Back to 68°F
        """
        original = 68
        back = C_to_Fahrenheit(K_to_celsius(F_to_kelvin(original)))
        _assert_close(back, original)

    # Physical constants
    def test_absolute_zero_conversions(self) -> None:
        """
        Test conversions at absolute zero.
        
        0K = -273.15°C = -459.67°F
        """
        abs_zero_C = Decimal("-273.15")
        _assert_close(C_to_kelvin(abs_zero_C), 0)
        _assert_close(C_to_Fahrenheit(abs_zero_C), "-459.67", "0.01")

    def test_water_freezing_point_all_scales(self) -> None:
        """
        Test water freezing point in all scales.
        
        0°C = 273.15K = 32°F
        """
        _assert_close(C_to_kelvin(0), "273.15")
        _assert_close(C_to_Fahrenheit(0), 32)

    def test_water_boiling_point_all_scales(self) -> None:
        """
        Test water boiling point in all scales.
        
        100°C = 373.15K = 212°F
        """
        _assert_close(C_to_kelvin(100), "373.15")
        _assert_close(C_to_Fahrenheit(100), 212)

    @pytest.mark.parametrize("celsius, kelvin, fahrenheit", [
        (Decimal("0"), Decimal("273.15"), Decimal("32")),
        (Decimal("100"), Decimal("373.15"), Decimal("212")),
        (Decimal("-40"), Decimal("233.15"), Decimal("-40")),
        (Decimal("25"), Decimal("298.15"), Decimal("77")),
        (Decimal("-273.15"), Decimal("0"), Decimal("-459.67")),
    ])
    def test_temp_triple_parametrized(
        self, celsius: Decimal, kelvin: Decimal, fahrenheit: Decimal
    ) -> None:
        """Parametrized test for temperature conversions across all three scales."""
        _assert_close(C_to_kelvin(celsius), kelvin, "1e-6")
        _assert_close(C_to_Fahrenheit(celsius), fahrenheit, "0.01")


# ============================================================================
# Lookup Tables
# ============================================================================

class TestTemperatureLookupTables:
    """Test suite for temperature conversion lookup tables."""

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
            assert isinstance(value[0], str)
            assert isinstance(value[1], str)
            assert callable(value[2])

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
            assert key not in temp_conv_funcs

    def test_temp_conv_funcs_rejects_invalid_unit_numbers(self) -> None:
        """
        Test that invalid temperature unit numbers are not in lookup table.
        
        Invalid: (0,1), (99,1), etc.
        """
        invalid_keys = [(0, 1), (1, 0), (99, 1), (1, 99)]
        for key in invalid_keys:
            assert key not in temp_conv_funcs


# ============================================================================
# Edge Cases, Physical Constants, Precision
# ============================================================================

class TestTemperatureEdgeCases:
    """Test edge cases and boundary conditions for temperature conversions."""

    def test_negative_kelvin_handling(self) -> None:
        """
        Test conversion from impossible negative Kelvin.
        
        Note: Tests mathematical conversion, not physical validity.
        Input: -10K
        Expected: Below absolute zero (unphysical but mathematically correct)
        """
        result = K_to_celsius(-10)
        assert result < Decimal("-273.15")

    def test_extreme_temperature_celsius(self) -> None:
        """
        Test conversions with extreme temperatures.
        
        Input: 1000°C
        Expected: 1273.15K, 1832°F
        """
        _assert_close(C_to_kelvin(1000), "1273.15")
        _assert_close(C_to_Fahrenheit(1000), 1832)

    def test_temperature_conversion_with_infinity(self) -> None:
        """
        Test temperature conversion with infinity.
        
        Input: float('inf')
        Expected: Result is infinity
        """
        assert C_to_kelvin(Decimal("Infinity")).is_infinite()
        assert C_to_Fahrenheit(Decimal("Infinity")).is_infinite()

    def test_temperature_conversion_with_nan(self) -> None:
        """
        Test temperature conversion with NaN.
        
        Input: float('nan')
        Expected: Result is NaN
        """
        assert C_to_kelvin(Decimal("NaN")).is_nan()

    def test_temperature_below_absolute_zero(self) -> None:
        """
        Test temperature conversion below absolute zero.
        
        Input: -300°C (below -273.15°C)
        Expected: Mathematically computed (negative Kelvin - unphysical)
        """
        result_k = C_to_kelvin(-300)
        assert isinstance(result_k, Decimal)
        assert result_k < 0


class TestTemperaturePhysicalConstants:
    """Test temperature conversions at known physical constants."""

    def test_body_temperature_conversions(self) -> None:
        """
        Test normal human body temperature.
        
        37°C = 310.15K = 98.6°F
        """
        _assert_close(C_to_kelvin(37), "310.15")
        _assert_close(C_to_Fahrenheit(37), "98.6", "0.1")

    def test_room_temperature_conversions(self) -> None:
        """
        Test standard room temperature.
        
        20°C = 293.15K = 68°F
        """
        _assert_close(C_to_kelvin(20), "293.15")
        _assert_close(C_to_Fahrenheit(20), 68, "1")


class TestTemperaturePrecision:
    """Test numerical precision and accuracy of temperature conversions."""

    def test_high_precision_temperature_conversion(self) -> None:
        """
        Test that temperature conversions maintain precision.
        
        Input: 0°C
        Expected: Exactly 273.15K
        """
        _assert_close(C_to_kelvin(0), "273.15", "1e-12")

    def test_multiple_conversion_precision_loss(self) -> None:
        """
        Test precision loss through multiple conversions.
        
        Action: C→K→C→F→C
        Expected: Minimal precision loss
        """
        original = Decimal("25.123456789")
        k = C_to_kelvin(original)
        c1 = K_to_celsius(k)
        f = C_to_Fahrenheit(c1)
        c2 = F_to_celsius(f)
        _assert_close(c2, original)

    def test_temperature_conversion_at_water_freezing_no_error(self) -> None:
        """
        Test conversion at water freezing point.
        
        Input: 0°C
        Expected: Exact conversions without errors
        """
        _assert_close(C_to_kelvin(0), "273.15", "1e-12")
        _assert_close(C_to_Fahrenheit(0), 32, "1e-12")

    def test_temperature_conversion_at_water_boiling_no_error(self) -> None:
        """
        Test conversion at water boiling point.
        
        Input: 100°C
        Expected: Exact conversions without errors
        """
        _assert_close(C_to_kelvin(100), "373.15", "1e-12")
        _assert_close(C_to_Fahrenheit(100), 212, "1e-12")


# ============================================================================
# Invalid Inputs
# ============================================================================

class TestTemperatureInvalidInputs:
    """Test invalid input handling for temperature conversion functions."""

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


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

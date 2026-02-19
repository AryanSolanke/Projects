"""
Pressure Converter Test Suite

Tests for pressure conversion functions covering all 6 units.

Coverage:
- convert_pressure() across all unit pairs
- Units: atm, bar, kPa, mmHg, Pa, psi
- Lookup tables: PRESSURE_UNIT_NAMES, PRESSURE_UNIT_ABBREV
- Round-trips, edge cases, physical constants, precision
"""

import pytest
from decimal import Decimal

from calculator.converters.pressure import (
    pressure_converter, pressure_conv_menuMsg,
    PRESSURE_UNIT_ABBREV, PRESSURE_UNIT_NAMES,
    PressureUnit, convert_pressure,
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

class TestPressureConversions:
    """Test suite for pressure conversion functions."""

    # Basic conversions to/from Pascal (base unit)
    def test_atm_to_pascal(self) -> None:
        """
        Test atmosphere to Pascal conversion.
        
        Input: 1 atm
        Expected: 101325 Pa
        """
        result = convert_pressure(1, PressureUnit.ATMOSPHERE, PressureUnit.PASCAL)
        _assert_close(result, 101325, "1e-6")

    def test_bar_to_pascal(self) -> None:
        """
        Test bar to Pascal conversion.
        
        Input: 1 bar
        Expected: 100000 Pa
        """
        result = convert_pressure(1, PressureUnit.BAR, PressureUnit.PASCAL)
        _assert_close(result, 100000, "1e-6")

    def test_kpa_to_pascal(self) -> None:
        """
        Test kilopascal to Pascal conversion.
        
        Input: 1 kPa
        Expected: 1000 Pa
        """
        result = convert_pressure(1, PressureUnit.KILOPASCAL, PressureUnit.PASCAL)
        _assert_close(result, 1000)

    def test_mmhg_to_pascal(self) -> None:
        """
        Test mmHg to Pascal conversion.
        
        Input: 1 mmHg
        Expected: 133.322 Pa
        """
        result = convert_pressure(1, PressureUnit.MM_MERCURY, PressureUnit.PASCAL)
        _assert_close(result, "133.322", "0.001")

    def test_psi_to_pascal(self) -> None:
        """
        Test PSI to Pascal conversion.
        
        Input: 1 psi
        Expected: 6894.76 Pa
        """
        result = convert_pressure(1, PressureUnit.PSI, PressureUnit.PASCAL)
        _assert_close(result, "6894.76", "0.01")

    # Common pressure conversions
    def test_atm_to_kpa(self) -> None:
        """
        Test atmosphere to kilopascal conversion.
        
        Input: 1 atm
        Expected: 101.325 kPa
        """
        result = convert_pressure(1, PressureUnit.ATMOSPHERE, PressureUnit.KILOPASCAL)
        _assert_close(result, "101.325", "0.001")

    def test_atm_to_bar(self) -> None:
        """
        Test atmosphere to bar conversion.
        
        Input: 1 atm
        Expected: 1.01325 bar
        """
        result = convert_pressure(1, PressureUnit.ATMOSPHERE, PressureUnit.BAR)
        _assert_close(result, "1.01325", "0.00001")

    def test_atm_to_mmhg(self) -> None:
        """
        Test atmosphere to mmHg conversion (mercury barometer).
        
        Input: 1 atm
        Expected: 760 mmHg
        """
        result = convert_pressure(1, PressureUnit.ATMOSPHERE, PressureUnit.MM_MERCURY)
        _assert_close(result, 760, "0.1")

    def test_atm_to_psi(self) -> None:
        """
        Test atmosphere to PSI conversion.
        
        Input: 1 atm
        Expected: 14.696 psi
        """
        result = convert_pressure(1, PressureUnit.ATMOSPHERE, PressureUnit.PSI)
        _assert_close(result, "14.696", "0.001")

    def test_bar_to_kpa(self) -> None:
        """
        Test bar to kilopascal conversion.
        
        Input: 1 bar
        Expected: 100 kPa
        """
        result = convert_pressure(1, PressureUnit.BAR, PressureUnit.KILOPASCAL)
        _assert_close(result, 100)

    def test_bar_to_atm(self) -> None:
        """
        Test bar to atmosphere conversion.
        
        Input: 1 bar
        Expected: 0.987 atm
        """
        result = convert_pressure(1, PressureUnit.BAR, PressureUnit.ATMOSPHERE)
        _assert_close(result, "0.986923", "0.0001")

    def test_psi_to_bar(self) -> None:
        """
        Test PSI to bar conversion.
        
        Input: 1 psi
        Expected: 0.0689476 bar
        """
        result = convert_pressure(1, PressureUnit.PSI, PressureUnit.BAR)
        _assert_close(result, "0.0689476", "0.00001")

    def test_psi_to_kpa(self) -> None:
        """
        Test PSI to kilopascal conversion.
        
        Input: 1 psi
        Expected: 6.89476 kPa
        """
        result = convert_pressure(1, PressureUnit.PSI, PressureUnit.KILOPASCAL)
        _assert_close(result, "6.89476", "0.0001")

    # Round-trip conversions
    def test_atm_to_pa_to_atm_roundtrip(self) -> None:
        """
        Test atmosphere → Pascal → atmosphere round-trip.
        
        Input: 2 atm
        Expected: Back to 2 atm after conversions
        """
        original = 2
        pascal = convert_pressure(original, PressureUnit.ATMOSPHERE, PressureUnit.PASCAL)
        back = convert_pressure(pascal, PressureUnit.PASCAL, PressureUnit.ATMOSPHERE)
        _assert_close(back, original)

    def test_psi_to_bar_to_psi_roundtrip(self) -> None:
        """
        Test PSI → bar → PSI round-trip.
        
        Input: 30 psi
        Expected: Back to 30 psi
        """
        original = 30
        bar = convert_pressure(original, PressureUnit.PSI, PressureUnit.BAR)
        back = convert_pressure(bar, PressureUnit.BAR, PressureUnit.PSI)
        _assert_close(back, original)

    def test_kpa_to_mmhg_to_kpa_roundtrip(self) -> None:
        """
        Test kPa → mmHg → kPa round-trip.
        
        Input: 100 kPa
        Expected: Back to 100 kPa
        """
        original = 100
        mmhg = convert_pressure(original, PressureUnit.KILOPASCAL, PressureUnit.MM_MERCURY)
        back = convert_pressure(mmhg, PressureUnit.MM_MERCURY, PressureUnit.KILOPASCAL)
        _assert_close(back, original, "1e-6")

    # Edge cases
    def test_zero_pressure_conversion(self) -> None:
        """
        Test conversion with zero pressure.
        
        Input: 0 atm
        Expected: 0 in all units
        """
        assert convert_pressure(0, PressureUnit.ATMOSPHERE, PressureUnit.PASCAL) == 0
        assert convert_pressure(0, PressureUnit.ATMOSPHERE, PressureUnit.PSI) == 0

    def test_negative_pressure_conversion(self) -> None:
        """
        Test conversion with negative pressure (vacuum/mathematical).
        
        Input: -1 atm
        Expected: Negative values in all units
        """
        assert convert_pressure(-1, PressureUnit.ATMOSPHERE, PressureUnit.PASCAL) < 0
        assert convert_pressure(-1, PressureUnit.ATMOSPHERE, PressureUnit.PSI) < 0

    def test_very_high_pressure_conversion(self) -> None:
        """
        Test conversion with very high pressure.
        
        Input: 10000 atm (deep ocean)
        Expected: Valid large values
        """
        result_pa = convert_pressure(10000, PressureUnit.ATMOSPHERE, PressureUnit.PASCAL)
        _assert_close(result_pa, 10000 * 101325, "1")

    def test_very_low_pressure_conversion(self) -> None:
        """
        Test conversion with very low pressure.
        
        Input: 0.001 atm
        Expected: 101.325 Pa
        """
        result = convert_pressure(Decimal("0.001"), PressureUnit.ATMOSPHERE, PressureUnit.PASCAL)
        _assert_close(result, "101.325", "0.001")

    # Physical constants and real-world scenarios
    def test_standard_atmospheric_pressure(self) -> None:
        """
        Test standard atmospheric pressure at sea level.
        
        1 atm = 101325 Pa = 101.325 kPa = 1.01325 bar = 760 mmHg = 14.696 psi
        """
        atm = 1
        _assert_close(convert_pressure(atm, PressureUnit.ATMOSPHERE, PressureUnit.PASCAL), 101325, "1")
        _assert_close(convert_pressure(atm, PressureUnit.ATMOSPHERE, PressureUnit.KILOPASCAL), "101.325", "0.001")
        _assert_close(convert_pressure(atm, PressureUnit.ATMOSPHERE, PressureUnit.BAR), "1.01325", "0.00001")
        _assert_close(convert_pressure(atm, PressureUnit.ATMOSPHERE, PressureUnit.MM_MERCURY), 760, "0.1")
        _assert_close(convert_pressure(atm, PressureUnit.ATMOSPHERE, PressureUnit.PSI), "14.696", "0.001")

    def test_tire_pressure_conversion(self) -> None:
        """
        Test typical car tire pressure conversion.
        
        32 psi ≈ 220.6 kPa ≈ 2.21 bar
        """
        psi = 32
        _assert_close(convert_pressure(psi, PressureUnit.PSI, PressureUnit.KILOPASCAL), "220.632", "0.1")
        _assert_close(convert_pressure(psi, PressureUnit.PSI, PressureUnit.BAR), "2.20632", "0.001")

    def test_blood_pressure_conversion(self) -> None:
        """
        Test blood pressure conversion (120/80 mmHg).
        
        120 mmHg ≈ 16 kPa
        """
        kpa = convert_pressure(120, PressureUnit.MM_MERCURY, PressureUnit.KILOPASCAL)
        _assert_close(kpa, "15.999", "0.01")

    def test_weather_pressure_high(self) -> None:
        """
        Test high weather pressure.
        
        1030 mbar = 1.03 bar = 103 kPa
        """
        kpa = convert_pressure(Decimal("1.03"), PressureUnit.BAR, PressureUnit.KILOPASCAL)
        _assert_close(kpa, 103)

    def test_scuba_diving_pressure(self) -> None:
        """
        Test scuba diving pressure at 10m depth.
        
        ~2 bar = 200 kPa ≈ 1.97 atm
        """
        bar = 2
        _assert_close(convert_pressure(bar, PressureUnit.BAR, PressureUnit.ATMOSPHERE), "1.97385", "0.001")
        _assert_close(convert_pressure(bar, PressureUnit.BAR, PressureUnit.KILOPASCAL), 200)

    # Parametrized tests
    @pytest.mark.parametrize("atm,expected_psi", [
        (Decimal("1"), Decimal("14.696")),
        (Decimal("2"), Decimal("29.392")),
        (Decimal("3"), Decimal("44.088")),
        (Decimal("0.5"), Decimal("7.348")),
    ])
    def test_atm_to_psi_parametrized(self, atm: Decimal, expected_psi: Decimal) -> None:
        """Parametrized test for atm to PSI conversions."""
        result = convert_pressure(atm, PressureUnit.ATMOSPHERE, PressureUnit.PSI)
        _assert_close(result, expected_psi, "0.01")

    @pytest.mark.parametrize("from_unit,to_unit,value,expected", [
        (PressureUnit.ATMOSPHERE, PressureUnit.PASCAL, Decimal("1"), Decimal("101325")),
        (PressureUnit.BAR, PressureUnit.KILOPASCAL, Decimal("1"), Decimal("100")),
        (PressureUnit.KILOPASCAL, PressureUnit.PASCAL, Decimal("1"), Decimal("1000")),
        (PressureUnit.ATMOSPHERE, PressureUnit.MM_MERCURY, Decimal("1"), Decimal("760")),
        (PressureUnit.BAR, PressureUnit.ATMOSPHERE, Decimal("1"), Decimal("0.986923")),
    ])
    def test_common_conversions_parametrized(
        self, from_unit: int, to_unit: int, value: Decimal, expected: Decimal
    ) -> None:
        """Parametrized test for common pressure conversions."""
        result = convert_pressure(value, from_unit, to_unit)
        _assert_close(result, expected, "0.01")

    # Precision tests
    def test_high_precision_atm_to_pascal(self) -> None:
        """
        Test that pressure conversions maintain high precision.
        
        Input: 1 atm
        Expected: Exactly 101325 Pa
        """
        result = convert_pressure(1, PressureUnit.ATMOSPHERE, PressureUnit.PASCAL)
        _assert_close(result, 101325, "1e-10")

    def test_multiple_conversion_precision(self) -> None:
        """
        Test precision through multiple conversions.
        
        Action: atm→Pa→kPa→bar→atm
        Expected: Minimal precision loss
        """
        original = Decimal("1.5")
        pa = convert_pressure(original, PressureUnit.ATMOSPHERE, PressureUnit.PASCAL)
        kpa = convert_pressure(pa, PressureUnit.PASCAL, PressureUnit.KILOPASCAL)
        bar = convert_pressure(kpa, PressureUnit.KILOPASCAL, PressureUnit.BAR)
        atm = convert_pressure(bar, PressureUnit.BAR, PressureUnit.ATMOSPHERE)
        _assert_close(atm, original)


# ============================================================================
# Lookup Tables
# ============================================================================

class TestPressureLookupTables:
    """Test suite for pressure converter lookup tables."""

    def test_pressure_unit_names_completeness(self) -> None:
        """
        Test that PRESSURE_UNIT_NAMES has all 6 units.
        
        Expected: All pressure units present
        """
        expected_units = [
            PressureUnit.ATMOSPHERE, PressureUnit.BAR,
            PressureUnit.KILOPASCAL, PressureUnit.MM_MERCURY,
            PressureUnit.PASCAL, PressureUnit.PSI,
        ]
        for unit in expected_units:
            assert unit in PRESSURE_UNIT_NAMES
            assert isinstance(PRESSURE_UNIT_NAMES[unit], str)
            assert len(PRESSURE_UNIT_NAMES[unit]) > 0

    def test_pressure_unit_abbrev_completeness(self) -> None:
        """
        Test that PRESSURE_UNIT_ABBREV has all 6 units.
        
        Expected: All abbreviations present
        """
        assert len(PRESSURE_UNIT_ABBREV) == 6
        for unit in PressureUnit:
            if unit != PressureUnit.QUIT:
                assert unit in PRESSURE_UNIT_ABBREV
                assert isinstance(PRESSURE_UNIT_ABBREV[unit], str)

    def test_pressure_unit_names_match_abbrev(self) -> None:
        """
        Test that names and abbreviations have matching keys.
        
        Expected: Same keys in both dictionaries
        """
        assert set(PRESSURE_UNIT_NAMES.keys()) == set(PRESSURE_UNIT_ABBREV.keys())


# ============================================================================
# Edge Cases and Invalid Inputs
# ============================================================================

class TestPressureEdgeCases:
    """Test edge cases and error scenarios for pressure conversion."""

    def test_same_unit_conversion(self) -> None:
        """
        Test conversion from unit to itself.
        
        Input: 5 atm to atm
        Expected: 5 atm (no change)
        """
        result = convert_pressure(5, PressureUnit.ATMOSPHERE, PressureUnit.ATMOSPHERE)
        _assert_close(result, 5, "1e-12")

    def test_pressure_conversion_with_infinity(self) -> None:
        """
        Test pressure conversion with infinity.
        
        Input: float('inf')
        Expected: Result is infinity
        """
        result = convert_pressure(Decimal("Infinity"), PressureUnit.ATMOSPHERE, PressureUnit.PSI)
        assert result.is_infinite()

    def test_pressure_conversion_with_nan(self) -> None:
        """
        Test pressure conversion with NaN.
        
        Input: float('nan')
        Expected: Result is NaN
        """
        result = convert_pressure(Decimal("NaN"), PressureUnit.ATMOSPHERE, PressureUnit.PASCAL)
        assert result.is_nan()

    def test_decimal_pressure_conversion(self) -> None:
        """
        Test conversion with decimal pressures.
        
        Input: 1.5 atm
        Expected: 151987.5 Pa
        """
        result = convert_pressure(Decimal("1.5"), PressureUnit.ATMOSPHERE, PressureUnit.PASCAL)
        _assert_close(result, "151987.5", "0.1")

    def test_fractional_pressure_conversion(self) -> None:
        """
        Test conversion with fractional pressures.
        
        Input: 0.5 bar
        Expected: 50 kPa
        """
        result = convert_pressure(Decimal("0.5"), PressureUnit.BAR, PressureUnit.KILOPASCAL)
        _assert_close(result, 50)


class TestPressureInvalidInputs:
    """Test invalid input handling for pressure conversions."""

    def test_invalid_from_unit_raises_error(self) -> None:
        """
        Test that invalid from_unit raises KeyError.
        
        Input: unit 99 (doesn't exist)
        Expected: KeyError
        """
        with pytest.raises(KeyError):
            convert_pressure(1, 99, PressureUnit.ATMOSPHERE)

    def test_invalid_to_unit_raises_error(self) -> None:
        """
        Test that invalid to_unit raises KeyError.
        
        Input: unit 0 (doesn't exist)
        Expected: KeyError
        """
        with pytest.raises(KeyError):
            convert_pressure(1, PressureUnit.ATMOSPHERE, 0)

    def test_string_pressure_raises_error(self) -> None:
        """
        Test that string pressure value raises TypeError.
        
        Input: "100" atm
        Expected: TypeError
        """
        with pytest.raises(TypeError):
            convert_pressure("100", PressureUnit.ATMOSPHERE, PressureUnit.PASCAL)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

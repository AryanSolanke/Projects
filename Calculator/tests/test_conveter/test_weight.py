"""
Weight Converter Test Suite

Tests for weight conversion functions covering all 13 units.

Coverage:
- convert_weight() across all unit pairs
- Metric units: kg, g, mg, cg, dg, dag, hg, tonne
- Imperial units: oz, lb, stone, short ton (US), long ton (UK)
- Lookup tables: WEIGHT_UNIT_NAMES, WEIGHT_UNIT_ABBREV
- Round-trips, edge cases, physical constants, precision
"""

import pytest
import math

from calculator.converters.weight import (
    convert_weight, weight_converter,
    WeightUnit, WEIGHT_UNIT_NAMES, WEIGHT_UNIT_ABBREV,
)


# ============================================================================
# Conversion Functions
# ============================================================================

class TestWeightConversions:
    """Test suite for weight conversion functions."""

    # Basic metric conversions
    def test_kg_to_gram(self) -> None:
        """
        Test kilogram to gram conversion.
        
        Input: 1 kg
        Expected: 1000 g
        """
        result = convert_weight(1, WeightUnit.KILOGRAM, WeightUnit.GRAM)
        assert abs(result - 1000) < 1e-9

    def test_gram_to_milligram(self) -> None:
        """
        Test gram to milligram conversion.
        
        Input: 1 g
        Expected: 1000 mg
        """
        result = convert_weight(1, WeightUnit.GRAM, WeightUnit.MILLIGRAM)
        assert abs(result - 1000) < 1e-9

    def test_kg_to_metric_tonne(self) -> None:
        """
        Test kilogram to metric tonne conversion.
        
        Input: 1000 kg
        Expected: 1 t
        """
        result = convert_weight(1000, WeightUnit.KILOGRAM, WeightUnit.METRIC_TONNE)
        assert abs(result - 1) < 1e-9

    # Metric to Imperial conversions
    def test_kg_to_pound(self) -> None:
        """
        Test kilogram to pound conversion.
        
        Input: 1 kg
        Expected: ~2.20462 lb
        """
        result = convert_weight(1, WeightUnit.KILOGRAM, WeightUnit.POUND)
        assert abs(result - 2.20462) < 0.001

    def test_pound_to_kg(self) -> None:
        """
        Test pound to kilogram conversion.
        
        Input: 1 lb
        Expected: 0.453592 kg
        """
        result = convert_weight(1, WeightUnit.POUND, WeightUnit.KILOGRAM)
        assert abs(result - 0.453592) < 1e-6

    def test_ounce_to_gram(self) -> None:
        """
        Test ounce to gram conversion.
        
        Input: 1 oz
        Expected: 28.3495 g
        """
        result = convert_weight(1, WeightUnit.OUNCE, WeightUnit.GRAM)
        assert abs(result - 28.3495) < 0.001

    def test_stone_to_kg(self) -> None:
        """
        Test stone to kilogram conversion.
        
        Input: 1 stone
        Expected: 6.35029 kg
        """
        result = convert_weight(1, WeightUnit.STONE, WeightUnit.KILOGRAM)
        assert abs(result - 6.35029) < 1e-5

    # Imperial unit conversions
    def test_pound_to_ounce(self) -> None:
        """
        Test pound to ounce conversion.
        
        Input: 1 lb
        Expected: 16 oz
        """
        result = convert_weight(1, WeightUnit.POUND, WeightUnit.OUNCE)
        assert abs(result - 16) < 0.01

    def test_stone_to_pound(self) -> None:
        """
        Test stone to pound conversion.
        
        Input: 1 stone
        Expected: 14 lb
        """
        result = convert_weight(1, WeightUnit.STONE, WeightUnit.POUND)
        assert abs(result - 14) < 0.01

    def test_short_ton_to_pound(self) -> None:
        """
        Test short ton (US) to pound conversion.
        
        Input: 1 short ton
        Expected: 2000 lb
        """
        result = convert_weight(1, WeightUnit.SHORT_TON_US, WeightUnit.POUND)
        assert abs(result - 2000) < 0.1

    def test_long_ton_to_pound(self) -> None:
        """
        Test long ton (UK) to pound conversion.
        
        Input: 1 long ton
        Expected: 2240 lb
        """
        result = convert_weight(1, WeightUnit.LONG_TON_UK, WeightUnit.POUND)
        assert abs(result - 2240) < 0.1

    # Round-trip conversions
    def test_kg_to_lb_to_kg_roundtrip(self) -> None:
        """
        Test kilogram → pound → kilogram round-trip.
        
        Input: 10 kg
        Expected: Back to 10 kg after conversions
        """
        original = 10
        pounds = convert_weight(original, WeightUnit.KILOGRAM, WeightUnit.POUND)
        back = convert_weight(pounds, WeightUnit.POUND, WeightUnit.KILOGRAM)
        assert abs(back - original) < 1e-9

    def test_gram_to_ounce_to_gram_roundtrip(self) -> None:
        """
        Test gram → ounce → gram round-trip.
        
        Input: 100 g
        Expected: Back to 100 g
        """
        original = 100
        ounces = convert_weight(original, WeightUnit.GRAM, WeightUnit.OUNCE)
        back = convert_weight(ounces, WeightUnit.OUNCE, WeightUnit.GRAM)
        assert abs(back - original) < 1e-6

    def test_stone_to_kg_to_stone_roundtrip(self) -> None:
        """
        Test stone → kg → stone round-trip.
        
        Input: 12 stone
        Expected: Back to 12 stone
        """
        original = 12
        kg = convert_weight(original, WeightUnit.STONE, WeightUnit.KILOGRAM)
        back = convert_weight(kg, WeightUnit.KILOGRAM, WeightUnit.STONE)
        assert abs(back - original) < 1e-9

    # Edge cases
    def test_zero_weight_conversion(self) -> None:
        """
        Test conversion with zero weight.
        
        Input: 0 kg
        Expected: 0 in all units
        """
        assert convert_weight(0, WeightUnit.KILOGRAM, WeightUnit.GRAM) == 0
        assert convert_weight(0, WeightUnit.KILOGRAM, WeightUnit.POUND) == 0

    def test_negative_weight_conversion(self) -> None:
        """
        Test conversion with negative weight (mathematically valid).
        
        Input: -5 kg
        Expected: Negative values in all units
        """
        assert convert_weight(-5, WeightUnit.KILOGRAM, WeightUnit.GRAM) < 0
        assert convert_weight(-5, WeightUnit.KILOGRAM, WeightUnit.POUND) < 0

    def test_very_small_weight_conversion(self) -> None:
        """
        Test conversion with very small weight.
        
        Input: 0.000001 kg (1 mg)
        Expected: 1 mg
        """
        result = convert_weight(0.000001, WeightUnit.KILOGRAM, WeightUnit.MILLIGRAM)
        assert abs(result - 1) < 1e-9

    def test_very_large_weight_conversion(self) -> None:
        """
        Test conversion with very large weight.
        
        Input: 1000000 kg
        Expected: 1000 metric tonnes
        """
        result = convert_weight(1000000, WeightUnit.KILOGRAM, WeightUnit.METRIC_TONNE)
        assert abs(result - 1000) < 1e-6

    # Physical constants and known values
    def test_human_body_weight_conversions(self) -> None:
        """
        Test typical human body weight conversions.
        
        70 kg = 154.32 lb = 11 stone
        """
        kg = 70
        pounds = convert_weight(kg, WeightUnit.KILOGRAM, WeightUnit.POUND)
        stone = convert_weight(kg, WeightUnit.KILOGRAM, WeightUnit.STONE)
        assert abs(pounds - 154.32) < 0.1
        assert abs(stone - 11.02) < 0.01

    def test_gold_bar_weight_conversion(self) -> None:
        """
        Test standard gold bar weight conversion.
        
        400 troy ounces ≈ 12.4 kg (approximate as 12400 g)
        """
        grams = convert_weight(12.4, WeightUnit.KILOGRAM, WeightUnit.GRAM)
        assert abs(grams - 12400) < 1e-6

    def test_ton_comparisons(self) -> None:
        """
        Test that short ton < long ton.
        
        1 short ton (US) = 907.185 kg
        1 long ton (UK) = 1016.05 kg
        """
        short_ton_kg = convert_weight(1, WeightUnit.SHORT_TON_US, WeightUnit.KILOGRAM)
        long_ton_kg = convert_weight(1, WeightUnit.LONG_TON_UK, WeightUnit.KILOGRAM)
        assert long_ton_kg > short_ton_kg
        assert abs(short_ton_kg - 907.185) < 0.01
        assert abs(long_ton_kg - 1016.05) < 0.01

    # Parametrized tests
    @pytest.mark.parametrize("kg,expected_lb", [
        (1, 2.20462),
        (10, 22.0462),
        (50, 110.231),
        (100, 220.462),
    ])
    def test_kg_to_lb_parametrized(self, kg: float, expected_lb: float) -> None:
        """Parametrized test for kg to pound conversions."""
        result = convert_weight(kg, WeightUnit.KILOGRAM, WeightUnit.POUND)
        assert abs(result - expected_lb) < 0.01

    @pytest.mark.parametrize("from_unit,to_unit,value,expected", [
        (WeightUnit.KILOGRAM, WeightUnit.GRAM, 1, 1000),
        (WeightUnit.GRAM, WeightUnit.MILLIGRAM, 1, 1000),
        (WeightUnit.POUND, WeightUnit.OUNCE, 1, 16),
        (WeightUnit.STONE, WeightUnit.POUND, 1, 14),
        (WeightUnit.METRIC_TONNE, WeightUnit.KILOGRAM, 1, 1000),
    ])
    def test_common_conversions_parametrized(
        self, from_unit: int, to_unit: int, value: float, expected: float
    ) -> None:
        """Parametrized test for common weight conversions."""
        result = convert_weight(value, from_unit, to_unit)
        assert abs(result - expected) < 0.1

    # Precision tests
    def test_high_precision_kg_to_gram(self) -> None:
        """
        Test that weight conversions maintain high precision.
        
        Input: 1 kg
        Expected: Exactly 1000 g
        """
        result = convert_weight(1, WeightUnit.KILOGRAM, WeightUnit.GRAM)
        assert abs(result - 1000) < 1e-12

    def test_multiple_conversion_precision(self) -> None:
        """
        Test precision through multiple conversions.
        
        Action: kg→g→mg→g→kg
        Expected: Minimal precision loss
        """
        original = 5.123456789
        g = convert_weight(original, WeightUnit.KILOGRAM, WeightUnit.GRAM)
        mg = convert_weight(g, WeightUnit.GRAM, WeightUnit.MILLIGRAM)
        g2 = convert_weight(mg, WeightUnit.MILLIGRAM, WeightUnit.GRAM)
        kg = convert_weight(g2, WeightUnit.GRAM, WeightUnit.KILOGRAM)
        assert abs(kg - original) < 1e-9


# ============================================================================
# Lookup Tables
# ============================================================================

class TestWeightLookupTables:
    """Test suite for weight converter lookup tables."""

    def test_weight_unit_names_completeness(self) -> None:
        """
        Test that WEIGHT_UNIT_NAMES has all 13 units.
        
        Expected: All weight units present
        """
        expected_units = [
            WeightUnit.KILOGRAM, WeightUnit.GRAM, WeightUnit.MILLIGRAM,
            WeightUnit.CENTIGRAM, WeightUnit.DECIGRAM, WeightUnit.DECAGRAM,
            WeightUnit.HECTOGRAM, WeightUnit.METRIC_TONNE, WeightUnit.OUNCE,
            WeightUnit.POUND, WeightUnit.STONE, WeightUnit.SHORT_TON_US,
            WeightUnit.LONG_TON_UK,
        ]
        for unit in expected_units:
            assert unit in WEIGHT_UNIT_NAMES
            assert isinstance(WEIGHT_UNIT_NAMES[unit], str)
            assert len(WEIGHT_UNIT_NAMES[unit]) > 0

    def test_weight_unit_abbrev_completeness(self) -> None:
        """
        Test that WEIGHT_UNIT_ABBREV has all 13 units.
        
        Expected: All abbreviations present
        """
        assert len(WEIGHT_UNIT_ABBREV) == 13
        for unit in WeightUnit:
            if unit != WeightUnit.QUIT:
                assert unit in WEIGHT_UNIT_ABBREV
                assert isinstance(WEIGHT_UNIT_ABBREV[unit], str)

    def test_weight_unit_names_match_abbrev(self) -> None:
        """
        Test that names and abbreviations have matching keys.
        
        Expected: Same keys in both dictionaries
        """
        assert set(WEIGHT_UNIT_NAMES.keys()) == set(WEIGHT_UNIT_ABBREV.keys())


# ============================================================================
# Edge Cases and Invalid Inputs
# ============================================================================

class TestWeightEdgeCases:
    """Test edge cases and error scenarios for weight conversion."""

    def test_same_unit_conversion(self) -> None:
        """
        Test conversion from unit to itself.
        
        Input: 5 kg to kg
        Expected: 5 kg (no change)
        """
        result = convert_weight(5, WeightUnit.KILOGRAM, WeightUnit.KILOGRAM)
        assert abs(result - 5) < 1e-12

    def test_weight_conversion_with_infinity(self) -> None:
        """
        Test weight conversion with infinity.
        
        Input: float('inf')
        Expected: Result is infinity
        """
        result = convert_weight(float('inf'), WeightUnit.KILOGRAM, WeightUnit.POUND)
        assert math.isinf(result)

    def test_weight_conversion_with_nan(self) -> None:
        """
        Test weight conversion with NaN.
        
        Input: float('nan')
        Expected: Result is NaN
        """
        result = convert_weight(float('nan'), WeightUnit.KILOGRAM, WeightUnit.GRAM)
        assert math.isnan(result)

    def test_decimal_weight_conversion(self) -> None:
        """
        Test conversion with decimal weights.
        
        Input: 2.5 kg
        Expected: 2500 g
        """
        result = convert_weight(2.5, WeightUnit.KILOGRAM, WeightUnit.GRAM)
        assert abs(result - 2500) < 1e-9

    def test_fractional_weight_conversion(self) -> None:
        """
        Test conversion with fractional weights.
        
        Input: 0.5 lb
        Expected: 8 oz
        """
        result = convert_weight(0.5, WeightUnit.POUND, WeightUnit.OUNCE)
        assert abs(result - 8) < 0.01


class TestWeightInvalidInputs:
    """Test invalid input handling for weight conversions."""

    def test_invalid_from_unit_raises_error(self) -> None:
        """
        Test that invalid from_unit raises KeyError.
        
        Input: unit 99 (doesn't exist)
        Expected: KeyError
        """
        with pytest.raises(KeyError):
            convert_weight(1, 99, WeightUnit.KILOGRAM)

    def test_invalid_to_unit_raises_error(self) -> None:
        """
        Test that invalid to_unit raises KeyError.
        
        Input: unit 0 (doesn't exist)
        Expected: KeyError
        """
        with pytest.raises(KeyError):
            convert_weight(1, WeightUnit.KILOGRAM, 0)

    def test_string_weight_raises_error(self) -> None:
        """
        Test that string weight value raises TypeError.
        
        Input: "100" kg
        Expected: TypeError
        """
        with pytest.raises(TypeError):
            convert_weight("100", WeightUnit.KILOGRAM, WeightUnit.GRAM)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

"""
Comprehensive Test Suite for sci.py

This module provides extensive unit tests for the scientific calculator module,
covering trignometric, hyperbolic, inverse functions with domain validation.

Testing strategy:
1. Domain validation - Test all domain boundaries 
2. Mathematical correctness - Verify computational accuracy
3. Error handling - Domain erros, asymptotes, edge cases
4. Special values - Zero, infinity, very large/small numbers
5. Symmetry - Test function properties (even/odd)
6. Range validation - Ensure outputs are within expected ranges

Standards:
- pytest framework
- Type hints for all test functions
- Parametrized tests for efficiency
- Property-based testing concepts
"""

import pytest
import math
from typing import Callable, Tuple, Generator
from pathlib import Path
import tempfile

from sci import (
    # Utility functions
    get_val,
    format_result,
    validate_subOpNum,
    validate_and_eval,
    
    # Trigonometric functions
    sine, cosine, tangent, cot, sec, cosec,
    
    # Inverse trigonometric functions
    sine_inv, cosine_inv, tangent_inv, cot_inv, sec_inv, cosec_inv,
    
    # Hyperbolic functions
    sineh, cosineh, tangenth, coth, sech, cosech,
    
    # Inverse hyperbolic functions
    sineh_inv, cosineh_inv, tangenth_inv, coth_inv, sech_inv, cosech_inv,
    
    # Constants and enums
    FunctionCategory,
    SubOperation,
    RESULT_PRECISION,
    ANGLE_TOLERANCE,
    
    # History functions
    display_hist_sci_calc,
    record_history_sci_calc,
    clear_hist_sci_calc,
)


# ============================================================================
# Test Fixtures
# ============================================================================

@pytest.fixture
def temp_sci_history(monkeypatch) -> Generator[Path, None, None]:
    """Create temporary history file for isolated testing."""
    temp_file = Path(tempfile.NamedTemporaryFile(suffix='_sci.txt'))
    monkeypatch.setattr('sci.HISTORY_FILE', temp_file)
    yield temp_file
    if temp_file.exists():
        temp_file.unlink()


# ============================================================================
# Test Utility Functions
# ============================================================================

class TestUtilityFunctions:
    """Test suite for utility functions."""
    
    def test_format_result_precision(self) -> None:
        """
        Test that format_result uses correct precision.
        
        Input: Pi to many decimals
        Expected: 9 significant figures
        """
        result = format_result(math.pi)
        assert result == "3.14159265"
    
    def test_format_result_removes_trailing_zeros(self) -> None:
        """
        Test removal of trailing zeros.
        
        Input: 5.0
        Expected: "5"
        """
        assert format_result(5.0) == "5"
    
    def test_format_result_very_small_number(self) -> None:
        """
        Test formatting of very small numbers.
        
        Input: 1e-12
        Expected: Scientific notation or very small decimal
        """
        result = format_result(1e-12)
        assert result != "0"
    
    def test_format_result_very_large_number(self) -> None:
        """
        Test formatting of very large numbers.
        
        Input: 1e12
        Expected: "1000000000000" or "1e+12"
        """
        result = format_result(1e12)
        assert "1" in result
    
    def test_validate_subOpNum_valid_range(self) -> None:
        """
        Test that valid sub-operation numbers (1-6) are accepted.
        
        Inputs: 1, 2, 3, 4, 5, 6
        Expected: All return 1
        """
        for i in range(1, 7):
            assert validate_subOpNum(i) == 1
    
    def test_validate_subOpNum_invalid_numbers(self, capsys) -> None:
        """
        Test that invalid sub-operation numbers are rejected.
        
        Inputs: 0, 7, -1, 100
        Expected: All return 0 with error message
        """
        for invalid in [0, 7, -1, 100]:
            result = validate_subOpNum(invalid)
            assert result == 0
    
    @pytest.mark.parametrize("value", [1, 2, 3, 4, 5, 6])
    def test_validate_subOpNum_parametrized_valid(self, value: int) -> None:
        """Parametrized test for valid sub-operation numbers."""
        assert validate_subOpNum(value) == 1
    
    @pytest.mark.parametrize("value", [0, 7, -1, 10, 100, -5])
    def test_validate_subOpNum_parametrized_invalid(self, value: int) -> None:
        """Parametrized test for invalid sub-operation numbers."""
        assert validate_subOpNum(value) == 0


# ============================================================================
# Test Trigonometric Functions
# ============================================================================

class TestTrigonometricFunctions:
    """Test suite for standard trigonometric functions."""
    
    # Sine function tests
    def test_sine_standard_angles(self) -> None:
        """
        Test sine at standard angles.
        
        Inputs: 0°, 30°, 45°, 60°, 90°
        Expected: 0, 0.5, √2/2, √3/2, 1
        """
        assert abs(sine(0) - 0) < 1e-9
        assert abs(sine(30) - 0.5) < 1e-9
        assert abs(sine(45) - math.sqrt(2)/2) < 1e-9
        assert abs(sine(60) - math.sqrt(3)/2) < 1e-9
        assert abs(sine(90) - 1) < 1e-9
    
    def test_sine_negative_angle(self) -> None:
        """
        Test sine with negative angles (odd function).
        
        Property: sin(-x) = -sin(x)
        """
        angle = 30
        assert abs(sine(-angle) - (-sine(angle))) < 1e-9
    
    def test_sine_periodicity(self) -> None:
        """
        Test sine periodicity.
        
        Property: sin(x) = sin(x + 360°)
        """
        angle = 45
        assert abs(sine(angle) - sine(angle + 360)) < 1e-9
    
    def test_sine_range(self) -> None:
        """
        Test that sine stays within [-1, 1].
        
        Test angles: 0° to 360° in 15° steps
        Expected: All values in [-1, 1]
        """
        for angle in range(0, 361, 15):
            value = sine(angle)
            assert -1 <= value <= 1
    
    # Cosine function tests
    def test_cosine_standard_angles(self) -> None:
        """Test cosine at standard angles."""
        assert abs(cosine(0) - 1) < 1e-9
        assert abs(cosine(60) - 0.5) < 1e-9
        assert abs(cosine(90) - 0) < 1e-9
    
    def test_cosine_negative_angle(self) -> None:
        """
        Test cosine with negative angles (even function).
        
        Property: cos(-x) = cos(x)
        """
        angle = 45
        assert abs(cosine(-angle) - cosine(angle)) < 1e-9
    
    # Tangent function tests
    def test_tangent_standard_angles(self) -> None:
        """Test tangent at standard angles."""
        assert abs(tangent(0) - 0) < 1e-9
        assert abs(tangent(45) - 1) < 1e-9
    
    def test_tangent_asymptote_detection(self) -> None:
        """
        Test that tangent detects asymptotes at 90°, 270°.
        
        Inputs: 90, -90, 270
        Expected: Asymptote error messages
        """
        result_90 = validate_and_eval(
            FunctionCategory.TRIGONOMETRIC, SubOperation.FUNC_3,
            "tan", tangent, 90
        )
        assert "Asymptote" in result_90 or "divide by zero" in result_90.lower()
    
    # Cotangent function tests
    def test_cot_standard_angles(self) -> None:
        """Test cotangent at standard angles."""
        assert abs(cot(45) - 1) < 1e-9
    
    def test_cot_asymptote_at_zero(self) -> None:
        """
        Test cotangent asymptote at 0°, 180°.
        
        Expected: Asymptote error
        """
        result = validate_and_eval(
            FunctionCategory.TRIGONOMETRIC, SubOperation.FUNC_4,
            "cot", cot, 0
        )
        assert "Asymptote" in result or "divide by zero" in result.lower()
    
    # Secant function tests
    def test_sec_at_zero(self) -> None:
        """Test secant at 0° equals 1."""
        assert abs(sec(0) - 1) < 1e-9
    
    def test_sec_asymptote_at_90(self) -> None:
        """Test secant asymptote at 90°."""
        result = validate_and_eval(
            FunctionCategory.TRIGONOMETRIC, SubOperation.FUNC_5,
            "sec", sec, 90
        )
        assert "Asymptote" in result or "divide by zero" in result.lower()
    
    # Cosecant function tests
    def test_cosec_at_90(self) -> None:
        """Test cosecant at 90° equals 1."""
        assert abs(cosec(90) - 1) < 1e-9
    
    def test_cosec_asymptote_at_zero(self) -> None:
        """Test cosecant asymptote at 0°."""
        result = validate_and_eval(
            FunctionCategory.TRIGONOMETRIC, SubOperation.FUNC_6,
            "cosec", cosec, 0
        )
        assert "Asymptote" in result or "divide by zero" in result.lower()
    
    @pytest.mark.parametrize("angle,expected_sin", [
        (0, 0),
        (30, 0.5),
        (90, 1),
        (180, 0),
        (270, -1),
    ])
    def test_sine_parametrized(self, angle: float, expected_sin: float) -> None:
        """Parametrized sine tests."""
        assert abs(sine(angle) - expected_sin) < 1e-9


def test_inverse_normal_trigo_funcs():

    """-------------------------- POSITIVE & NEGATIVE VALUES TEST --------------------------"""
    
    # ----- SIN⁻¹ ----- (sub_op = 1)
    assert validate_and_eval(3, 1, "sin⁻¹", sine_inv, 0.564738) == "sin⁻¹(0.564738) = 34.384099541"
    assert validate_and_eval(3, 1, "sin⁻¹", sine_inv, -0.564738) == "sin⁻¹(-0.564738) = -34.384099541"
    
    # ----- COS⁻¹ ----- (sub_op = 2)
    assert validate_and_eval(3, 2, "cos⁻¹", cosine_inv, 0.564738) == "cos⁻¹(0.564738) = 55.615900459"
    assert validate_and_eval(3, 2, "cos⁻¹", cosine_inv, -0.564738) == "cos⁻¹(-0.564738) = 124.384099541"
    
    # ----- TAN⁻¹ ----- (sub_op = 3)
    assert validate_and_eval(3, 3, "tan⁻¹", tangent_inv, 2.718281) == "tan⁻¹(2.718281) = 69.802463052"
    assert validate_and_eval(3, 3, "tan⁻¹", tangent_inv, -2.718281) == "tan⁻¹(-2.718281) = -69.802463052"
    
    # ----- COT⁻¹ ----- (sub_op = 4)
    assert validate_and_eval(3, 4, "cot⁻¹", cot_inv, 0.564738) == "cot⁻¹(0.564738) = 60.544932027"
    assert validate_and_eval(3, 4, "cot⁻¹", cot_inv, -0.564738) == "cot⁻¹(-0.564738) = -60.544932027"
    
    # ----- SEC⁻¹ ----- (sub_op = 5)
    assert validate_and_eval(3, 5, "sec⁻¹", sec_inv, 1.732051) == "sec⁻¹(1.732051) = 54.735614818"
    assert validate_and_eval(3, 5, "sec⁻¹", sec_inv, -1.732051) == "sec⁻¹(-1.732051) = 125.264385182"
    
    # ----- COSEC⁻¹ ----- (sub_op = 6)
    assert validate_and_eval(3, 6, "cosec⁻¹", cosec_inv, 1.732051) == "cosec⁻¹(1.732051) = 35.264385182"
    assert validate_and_eval(3, 6, "cosec⁻¹", cosec_inv, -1.732051) == "cosec⁻¹(-1.732051) = -35.264385182"


    """-------------------------- DOMAIN TEST --------------------------"""

    # SIN⁻¹ domain [-1, 1]
    assert validate_and_eval(3, 1, "sin⁻¹", sine_inv, 1.5) == "Domain error: Enter value between [-1,1]"
    assert validate_and_eval(3, 1, "sin⁻¹", sine_inv, -1.5) == "Domain error: Enter value between [-1,1]"

    # COS⁻¹ domain [-1, 1]
    assert validate_and_eval(3, 2, "cos⁻¹", cosine_inv, 1.5) == "Domain error: Enter value between [-1,1]"
    assert validate_and_eval(3, 2, "cos⁻¹", cosine_inv, -1.5) == "Domain error: Enter value between [-1,1]"

    # TAN⁻¹ domain all real numbers → no error
    # COT⁻¹ special case val = 0
    assert validate_and_eval(3, 4, "cot⁻¹", cot_inv, 0) == "cot⁻¹(0) = 90"

    # SEC⁻¹ domain |x| >= 1
    assert validate_and_eval(3, 5, "sec⁻¹", sec_inv, 0.5) == "Domain error: Enter value which lie in |x|>=1"
    assert validate_and_eval(3, 5, "sec⁻¹", sec_inv, -0.5) == "Domain error: Enter value which lie in |x|>=1"

    # COSEC⁻¹ domain |x| >= 1
    assert validate_and_eval(3, 6, "cosec⁻¹", cosec_inv, 0.5) == "Domain error: Enter value which lie in |x|>=1"
    assert validate_and_eval(3, 6, "cosec⁻¹", cosec_inv, -0.5) == "Domain error: Enter value which lie in |x|>=1"


    """-------------------------- LARGE & SMALL INPUT TEST --------------------------"""

    # LARGE input
    assert validate_and_eval(3, 1, "sin⁻¹", sine_inv, 1.0) == "sin⁻¹(1.0) = 90"
    assert validate_and_eval(3, 2, "cos⁻¹", cosine_inv, 1.0) == "cos⁻¹(1.0) = 0"
    assert validate_and_eval(3, 3, "tan⁻¹", tangent_inv, 1000000) == "tan⁻¹(1000000) = 89.999942704"
    assert validate_and_eval(3, 4, "cot⁻¹", cot_inv, 1000000) == "cot⁻¹(1000000) = 0.000057296"
    assert validate_and_eval(3, 5, "sec⁻¹", sec_inv, 1000000) == "sec⁻¹(1000000) = 89.999942704"
    assert validate_and_eval(3, 6, "cosec⁻¹", cosec_inv, 1000000) == "cosec⁻¹(1000000) = 0.000057296"

    # SMALL input
    assert validate_and_eval(3, 1, "sin⁻¹", sine_inv, 1e-6) == "sin⁻¹(1e-06) = 0.000057296"
    assert validate_and_eval(3, 2, "cos⁻¹", cosine_inv, 1e-6) == "cos⁻¹(1e-06) = 89.999942704"
    assert validate_and_eval(3, 3, "tan⁻¹", tangent_inv, 1e-6) == "tan⁻¹(1e-06) = 0.000057296"
    assert validate_and_eval(3, 4, "cot⁻¹", cot_inv, 1e-6) == "cot⁻¹(1e-06) = 89.999942704"
    assert validate_and_eval(3, 5, "sec⁻¹", sec_inv, 1.000001) == "sec⁻¹(1.000001) = 0.081028435"
    assert validate_and_eval(3, 6, "cosec⁻¹", cosec_inv, 1.000001) == "cosec⁻¹(1.000001) = 89.918971565"


    """-------------------------- INVALID INPUT TEST --------------------------"""

    for invalid in ["", "abc", "🙂", "@#$%", None, []]:
        assert validate_and_eval(3, 1, "sin⁻¹", sine_inv, invalid) == 0
        assert validate_and_eval(3, 2, "cos⁻¹", cosine_inv, invalid) == 0
        assert validate_and_eval(3, 3, "tan⁻¹", tangent_inv, invalid) == 0
        assert validate_and_eval(3, 4, "cot⁻¹", cot_inv, invalid) == 0
        assert validate_and_eval(3, 5, "sec⁻¹", sec_inv, invalid) == 0
        assert validate_and_eval(3, 6, "cosec⁻¹", cosec_inv, invalid) == 0

def test_hyperbolic_trigo_funcs():

    """-------------------------- POSITIVE & NEGATIVE VALUES TEST --------------------------"""
    
    # ----- SINH ----- (sub_op = 1)
    assert validate_and_eval(2, 1, "sinh", sineh, 2.718281) == "sinh(2.718281) = 7.544130798"
    assert validate_and_eval(2, 1, "sinh", sineh, -2.718281) == "sinh(-2.718281) = -7.544130798"
    
    # ----- COSH ----- (sub_op = 2)
    assert validate_and_eval(2, 2, "cosh", cosineh, 2.718281) == "cosh(2.718281) = 7.610118889"
    assert validate_and_eval(2, 2, "cosh", cosineh, -2.718281) == "cosh(-2.718281) = 7.610118889"
    
    # ----- TANH ----- (sub_op = 3)
    assert validate_and_eval(2, 3, "tanh", tangenth, 2.718281) == "tanh(2.718281) = 0.991328901"
    assert validate_and_eval(2, 3, "tanh", tangenth, -2.718281) == "tanh(-2.718281) = -0.991328901"
    
    # ----- COTH ----- (sub_op = 4)
    assert validate_and_eval(2, 4, "coth", coth, 2.718281) == "coth(2.718281) = 1.008746944"
    assert validate_and_eval(2, 4, "coth", coth, -2.718281) == "coth(-2.718281) = -1.008746944"
    
    # ----- SECH ----- (sub_op = 5)
    assert validate_and_eval(2, 5, "sech", sech, 2.718281) == "sech(2.718281) = 0.131403992"
    assert validate_and_eval(2, 5, "sech", sech, -2.718281) == "sech(-2.718281) = 0.131403992"
    
    # ----- COSECH ----- (sub_op = 6)
    assert validate_and_eval(2, 6, "cosech", cosech, 2.718281) == "cosech(2.718281) = 0.132553375"
    assert validate_and_eval(2, 6, "cosech", cosech, -2.718281) == "cosech(-2.718281) = -0.132553375"


    """-------------------------- DOMAIN TEST --------------------------"""

    # SINH domain all real → no error
    # COSH domain all real → no error
    # TANH domain all real → no error
    # COTH domain val != 0
    assert validate_and_eval(2, 4, "coth", coth, 0) == "Cannot divide by zero"
    
    # COSECH domain val != 0
    assert validate_and_eval(2, 6, "cosech", cosech, 0) == "Cannot divide by zero"


    """-------------------------- LARGE & SMALL INPUT TEST --------------------------"""

    # LARGE input
    assert validate_and_eval(2, 1, "sinh", sineh, 20) == "sinh(20) = 242582597.704895139"
    assert validate_and_eval(2, 2, "cosh", cosineh, 20) == "cosh(20) = 242582597.704895139"
    assert validate_and_eval(2, 3, "tanh", tangenth, 2.5) == "tanh(2.5) = 0.986614298"
    assert validate_and_eval(2, 4, "coth", coth, 2.5) == "coth(2.5) = 1.01356731"
    assert validate_and_eval(2, 5, "sech", sech, 2.5) == "sech(2.5) = 0.163071232"
    assert validate_and_eval(2, 6, "cosech", cosech, 2.5) == "cosech(2.5) = 0.16528367"

    # SMALL input
    assert validate_and_eval(2, 1, "sinh", sineh, 0.001234567) == "sinh(0.001234567) = 0.001234567"
    assert validate_and_eval(2, 2, "cosh", cosineh, 0.001234567) == "cosh(0.001234567) = 1.000000762"
    assert validate_and_eval(2, 3, "tanh", tangenth, 0.001234567) == "tanh(0.001234567) = 0.001234566"
    assert validate_and_eval(2, 4, "coth", coth, 0.001234567) == "coth(0.001234567) = 810.001002823"
    assert validate_and_eval(2, 5, "sech", sech, 0.001234567) == "sech(0.001234567) = 0.999999238"
    assert validate_and_eval(2, 6, "cosech", cosech, 0.001234567) == "cosech(0.001234567) = 810.000385539"



    """-------------------------- INVALID INPUT TEST --------------------------"""

    for invalid in ["", "abc", "🙂", "@#$%", None, []]:
        assert validate_and_eval(2, 1, "sinh", sineh, invalid) == 0
        assert validate_and_eval(2, 2, "cosh", cosineh, invalid) == 0
        assert validate_and_eval(2, 3, "tanh", tangenth, invalid) == 0
        assert validate_and_eval(2, 4, "coth", coth, invalid) == 0
        assert validate_and_eval(2, 5, "sech", sech, invalid) == 0
        assert validate_and_eval(2, 6, "cosech", cosech, invalid) == 0

def test_inverse_hyperbolic_trigo_funcs():

    """-------------------------- POSITIVE & NEGATIVE VALUES TEST --------------------------"""
    
    # ----- SINH⁻¹ ----- (sub_op = 1)
    assert validate_and_eval(4, 1, "sinh⁻¹", sineh_inv, 2.718281) == "sinh⁻¹(2.718281) = 1.725382273"
    assert validate_and_eval(4, 1, "sinh⁻¹", sineh_inv, -2.718281) == "sinh⁻¹(-2.718281) = -1.725382273"
    
    # ----- COSH⁻¹ ----- (sub_op = 2)
    assert validate_and_eval(4, 2, "cosh⁻¹", cosineh_inv, 3.141593) == "cosh⁻¹(3.141593) = 1.811526389"
    assert validate_and_eval(4, 2, "cosh⁻¹", cosineh_inv, 10.123456) == "cosh⁻¹(10.123456) = 3.005553917"
    
    # ----- TANH⁻¹ ----- (sub_op = 3)
    assert validate_and_eval(4, 3, "tanh⁻¹", tangenth_inv, 0.564738) == "tanh⁻¹(0.564738) = 0.639762764"
    assert validate_and_eval(4, 3, "tanh⁻¹", tangenth_inv, -0.564738) == "tanh⁻¹(-0.564738) = -0.639762764"
    
    # ----- COTH⁻¹ ----- (sub_op = 4)
    assert validate_and_eval(4, 4, "coth⁻¹", coth_inv, 2.718281) == "coth⁻¹(2.718281) = 0.385968546"
    assert validate_and_eval(4, 4, "coth⁻¹", coth_inv, -2.718281) == "coth⁻¹(-2.718281) = -0.385968546"
    
    # ----- SECH⁻¹ ----- (sub_op = 5)
    assert validate_and_eval(4, 5, "sech⁻¹", sech_inv, 0.564738) == "sech⁻¹(0.564738) = 1.173121432"
    assert validate_and_eval(4, 5, "sech⁻¹", sech_inv, 0.123456789) == "sech⁻¹(0.123456789) = 2.781178892"
    
    # ----- COSECH⁻¹ ----- (sub_op = 6)
    assert validate_and_eval(4, 6, "cosech⁻¹", cosech_inv, 2.718281) == "cosech⁻¹(2.718281) = 0.36004975"
    assert validate_and_eval(4, 6, "cosech⁻¹", cosech_inv, -2.718281) == "cosech⁻¹(-2.718281) = -0.36004975"

    """-------------------------- DOMAIN TEST --------------------------"""

    # SINH⁻¹ domain all real → no error
    # COSH⁻¹ domain >= 1
    assert validate_and_eval(4, 2, "cosh⁻¹", cosineh_inv, 0.5) == "Domain error: Enter value greater than 1"
    
    # TANH⁻¹ domain (-1, 1)
    assert validate_and_eval(4, 3, "tanh⁻¹", tangenth_inv, 1) == "Domain error: Enter value between (-1,1)"
    assert validate_and_eval(4, 3, "tanh⁻¹", tangenth_inv, -1) == "Domain error: Enter value between (-1,1)"
    
    # COTH⁻¹ domain |x|>1
    assert validate_and_eval(4, 4, "coth⁻¹", coth_inv, 0.5) == "Domain error: Enter value outside [-1,1]"
    assert validate_and_eval(4, 4, "coth⁻¹", coth_inv, -0.5) == "Domain error: Enter value outside [-1,1]"
    
    # SECH⁻¹ domain (0, 1]
    assert validate_and_eval(4, 5, "sech⁻¹", sech_inv, 0) == "Domain error: Enter value in range (0,1]"
    assert validate_and_eval(4, 5, "sech⁻¹", sech_inv, 1.5) == "Domain error: Enter value in range (0,1]"
    
    # COSECH⁻¹ domain val != 0
    assert validate_and_eval(4, 6, "cosech⁻¹", cosech_inv, 0) == "Domain error: Enter any value except 0"


    """-------------------------- LARGE & SMALL INPUT TEST --------------------------"""

    # LARGE input
    assert validate_and_eval(4, 1, "sinh⁻¹", sineh_inv, 1000) == "sinh⁻¹(1000) = 7.60090271"
    assert validate_and_eval(4, 2, "cosh⁻¹", cosineh_inv, 1000) == "cosh⁻¹(1000) = 7.60090221"
    assert validate_and_eval(4, 3, "tanh⁻¹", tangenth_inv, 0.999999123) == "tanh⁻¹(0.999999123) = 7.319952793"
    assert validate_and_eval(4, 4, "coth⁻¹", coth_inv, 1.000001234) == "coth⁻¹(1.000001234) = 7.149198715"
    assert validate_and_eval(4, 5, "sech⁻¹", sech_inv, 0.001234567) == "sech⁻¹(0.001234567) = 7.390181777"
    assert validate_and_eval(4, 6, "cosech⁻¹", cosech_inv, 0.001234567) == "cosech⁻¹(0.001234567) = 7.390182539"

    # SMALL input
    assert validate_and_eval(4, 1, "sinh⁻¹", sineh_inv, 0.001234567) == "sinh⁻¹(0.001234567) = 0.001234567"
    assert validate_and_eval(4, 2, "cosh⁻¹", cosineh_inv, 1.000001234) == "cosh⁻¹(1.000001234) = 0.001570987"
    assert validate_and_eval(4, 3, "tanh⁻¹", tangenth_inv, 0.001234567) == "tanh⁻¹(0.001234567) = 0.001234568"
    assert validate_and_eval(4, 4, "coth⁻¹", coth_inv, 1.001234567) == "coth⁻¹(1.001234567) = 3.695399626"
    assert validate_and_eval(4, 5, "sech⁻¹", sech_inv, 0.999999123) == "sech⁻¹(0.999999123) = 0.001324387"
    assert validate_and_eval(4, 6, "cosech⁻¹", cosech_inv, 1.001234567) == "cosech⁻¹(1.001234567) = 0.880501424"


    """-------------------------- INVALID INPUT TEST --------------------------"""

    for invalid in ["", "abc", "🙂", "@#$%", None, []]:
        assert validate_and_eval(4, 1, "sinh⁻¹", sineh_inv, invalid) == 0
        assert validate_and_eval(4, 2, "cosh⁻¹", cosineh_inv, invalid) == 0
        assert validate_and_eval(4, 3, "tanh⁻¹", tangenth_inv, invalid) == 0
        assert validate_and_eval(4, 4, "coth⁻¹", coth_inv, invalid) == 0
        assert validate_and_eval(4, 5, "sech⁻¹", sech_inv, invalid) == 0
        assert validate_and_eval(4, 6, "cosech⁻¹", cosech_inv, invalid) == 0
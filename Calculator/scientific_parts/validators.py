"""Domain and asymptote validators for scientific functions."""

from decimal import Decimal

from calculator.exceptions import AsymptoteError, DomainError
from calculator.scientific_parts.core import ANGLE_TOLERANCE, SubOperation, _to_decimal


def validate_trig_asymptote(sub_op_num: int, angle) -> None:
    """Check asymptotes in regular trigonometric functions."""
    angle_dec = _to_decimal(angle)
    mod_180 = angle_dec % Decimal(180)
    if sub_op_num in (SubOperation.FUNC_4, SubOperation.FUNC_6):
        if abs(mod_180) <= ANGLE_TOLERANCE or abs(mod_180 - Decimal(180)) <= ANGLE_TOLERANCE:
            raise AsymptoteError("Asymptote Error: Division by zero (Asymptote at n*180°)")
    if sub_op_num in (SubOperation.FUNC_3, SubOperation.FUNC_5):
        if abs(mod_180 - Decimal(90)) <= ANGLE_TOLERANCE:
            raise AsymptoteError("Asymptote Error: Division by zero (Asymptote at n*180° + 90°)")


def validate_hyperbolic_asymptote(sub_op_num: int, val) -> None:
    """Check asymptotes in hyperbolic functions."""
    val_dec = _to_decimal(val)
    if sub_op_num in (SubOperation.FUNC_4, SubOperation.FUNC_6) and val_dec == 0:
        raise AsymptoteError("Asymptote Error: Division by zero (Undefined at x=0)")


def validate_inverse_trig_domain(sub_op_num: int, val) -> None:
    """Validate domain for inverse trigonometric functions."""
    val_dec = _to_decimal(val)
    if sub_op_num in (SubOperation.FUNC_1, SubOperation.FUNC_2):
        if val_dec < -1 or val_dec > 1:
            raise DomainError("Domain Error: Input x must satisfy |x| <= 1")
    if sub_op_num in (SubOperation.FUNC_5, SubOperation.FUNC_6):
        if -1 < val_dec < 1:
            raise DomainError("Domain Error: Input x must satisfy |x| >= 1")


def validate_inverse_hyperbolic_domain(sub_op_num: int, val) -> None:
    """Validate domain for inverse hyperbolic functions."""
    domain_checks = {
        SubOperation.FUNC_2: (
            lambda x: x < 1,
            "Domain Error: acosh(x) requires x >= 1",
        ),
        SubOperation.FUNC_3: (
            lambda x: x <= -1 or x >= 1,
            "Domain Error: atanh(x) requires x in open interval (-1, 1)",
        ),
        SubOperation.FUNC_4: (
            lambda x: -1 <= x <= 1,
            "Domain Error: acoth(x) requires x outside closed interval [-1, 1]",
        ),
        SubOperation.FUNC_5: (
            lambda x: x <= 0 or x > 1,
            "Domain Error: asech(x) requires x in range (0, 1]",
        ),
        SubOperation.FUNC_6: (
            lambda x: x == 0,
            "Domain Error: acosech(x) is undefined at x=0",
        ),
    }

    if sub_op_num in domain_checks:
        check_func, error_msg = domain_checks[sub_op_num]
        if check_func(_to_decimal(val)):
            raise DomainError(error_msg)




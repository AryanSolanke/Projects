"""Core primitives for scientific calculator computations."""

from decimal import Decimal, InvalidOperation, localcontext
from enum import IntEnum

from calculator.config import DISPLAY_PRECISION, INTERNAL_PRECISION
from calculator.exceptions import DomainError, ExpressionError, InvalidInputError

NumberLike = Decimal | int | str
RESULT_PRECISION = DISPLAY_PRECISION
ANGLE_TOLERANCE = Decimal("1e-9")


class FunctionCategory(IntEnum):
    """Enumeration of function categories for routing and validation."""

    TRIGONOMETRIC = 1
    HYPERBOLIC = 2
    INVERSE_TRIGONOMETRIC = 3
    INVERSE_HYPERBOLIC = 4


class SciOperation(IntEnum):
    """Scientific calculator operations."""

    TRIG = 1
    INVERSE_TRIG = 2
    HYPERBOLIC = 3
    INVERSE_HYPERBOLIC = 4
    SHOW_MENU = 5
    SHOW_HISTORY = 6
    CLEAR_HISTORY = 7
    QUIT = 8


class SubOperation(IntEnum):
    """Enumeration of sub-operations within each category."""

    FUNC_1 = 1
    FUNC_2 = 2
    FUNC_3 = 3
    FUNC_4 = 4
    FUNC_5 = 5
    FUNC_6 = 6


def _to_decimal(value: NumberLike) -> Decimal:
    if isinstance(value, Decimal):
        return value
    if isinstance(value, int):
        return Decimal(value)
    try:
        return Decimal(str(value))
    except InvalidOperation:
        raise ExpressionError()
    except (TypeError, ValueError):
        raise InvalidInputError("Invalid Value: Please use numbers only.")


def compute_pi() -> Decimal:
    """Compute pi using the Gauss-Legendre algorithm."""
    with localcontext() as ctx:
        ctx.prec = INTERNAL_PRECISION
        a = Decimal(1)
        b = Decimal(1) / Decimal(2).sqrt()
        t = Decimal(1) / Decimal(4)
        p = Decimal(1)
        for _ in range(7):
            an = (a + b) / 2
            b = (a * b).sqrt()
            t = t - p * (a - an) * (a - an)
            a = an
            p = p * 2
        return (a + b) * (a + b) / (Decimal(4) * t)


PI = compute_pi()
TWO_PI = PI * 2


def _radians(angle: Decimal) -> Decimal:
    return angle * PI / Decimal(180)


def _degrees(rad: Decimal) -> Decimal:
    return rad * Decimal(180) / PI


def _reduce_radians(x: Decimal) -> Decimal:
    y = x % TWO_PI
    if y > PI:
        y -= TWO_PI
    return y


def _sin_decimal(x: Decimal) -> Decimal:
    with localcontext() as ctx:
        ctx.prec = INTERNAL_PRECISION
        x = _reduce_radians(x)
        term = x
        result = Decimal(0)
        n = 1
        eps = Decimal(10) ** (-(INTERNAL_PRECISION - 5))
        while True:
            result += term
            term *= -x * x / (Decimal(2 * n) * Decimal(2 * n + 1))
            if abs(term) < eps:
                break
            n += 1
        return +result


def _cos_decimal(x: Decimal) -> Decimal:
    with localcontext() as ctx:
        ctx.prec = INTERNAL_PRECISION
        x = _reduce_radians(x)
        term = Decimal(1)
        result = Decimal(0)
        n = 1
        eps = Decimal(10) ** (-(INTERNAL_PRECISION - 5))
        while True:
            result += term
            term *= -x * x / (Decimal(2 * n - 1) * Decimal(2 * n))
            if abs(term) < eps:
                break
            n += 1
        return +result


def _atan_decimal(x: Decimal) -> Decimal:
    with localcontext() as ctx:
        ctx.prec = INTERNAL_PRECISION
        if x == 0:
            return Decimal(0)
        if abs(x) > 1:
            sign = Decimal(1) if x > 0 else Decimal(-1)
            return sign * (PI / 2) - _atan_decimal(Decimal(1) / x)
        term = x
        result = term
        n = 1
        eps = Decimal(10) ** (-(INTERNAL_PRECISION - 5))
        while True:
            term *= -x * x * Decimal(2 * n - 1) / Decimal(2 * n + 1)
            if abs(term) < eps:
                break
            result += term
            n += 1
        return +result


def _asin_decimal(x: Decimal) -> Decimal:
    with localcontext() as ctx:
        ctx.prec = INTERNAL_PRECISION
        if x == 0:
            return Decimal(0)
        if abs(x) > 1:
            raise DomainError("Domain Error: Input x must satisfy |x| <= 1")
        if x == 1:
            return PI / 2
        if x == -1:
            return -PI / 2
        return _atan_decimal(x / (Decimal(1) - x * x).sqrt())


def _acos_decimal(x: Decimal) -> Decimal:
    return PI / 2 - _asin_decimal(x)


def _exp_decimal(x: Decimal) -> Decimal:
    return x.exp()


def _ln_decimal(x: Decimal) -> Decimal:
    return x.ln()


def _sinh_decimal(x: Decimal) -> Decimal:
    ex = _exp_decimal(x)
    exn = _exp_decimal(-x)
    return (ex - exn) / 2


def _cosh_decimal(x: Decimal) -> Decimal:
    ex = _exp_decimal(x)
    exn = _exp_decimal(-x)
    return (ex + exn) / 2


def _tanh_decimal(x: Decimal) -> Decimal:
    return _sinh_decimal(x) / _cosh_decimal(x)


def _asinh_decimal(x: Decimal) -> Decimal:
    return _ln_decimal(x + (x * x + 1).sqrt())


def _acosh_decimal(x: Decimal) -> Decimal:
    return _ln_decimal(x + (x - 1).sqrt() * (x + 1).sqrt())


def _atanh_decimal(x: Decimal) -> Decimal:
    return _ln_decimal((1 + x) / (1 - x)) / 2


def format_result(result: NumberLike) -> str:
    """Format numerical result using configured significant precision."""
    return f"{result:.{RESULT_PRECISION}g}"


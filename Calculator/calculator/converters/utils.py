"""
Converter Utilities

Shared helpers for converter modules.
"""

from __future__ import annotations

from decimal import Decimal
import math
from typing import Optional


def to_decimal(value: float | int | Decimal, value_type: str = "Value") -> Decimal:
    """
    Convert numeric values to Decimal with type checking.

    Args:
        value: Numeric value to convert
        value_type: Name of value for error messages

    Returns:
        Decimal representation
    """
    if isinstance(value, Decimal):
        return value
    if isinstance(value, (int, float)):
        return Decimal(str(value))
    raise TypeError(f"{value_type} must be numeric (int, float, or Decimal), got {type(value).__name__}")


def get_numeric_input(prompt: str = "") -> Optional[float]:
    """
    Prompt user for numeric input with error handling.

    Args:
        prompt: Input prompt message

    Returns:
        Float value if valid, None otherwise
    """
    try:
        raw = input(prompt).strip()
        if raw == "":
            return None
        return float(raw)
    except (ValueError, TypeError):
        return None


def format_numeric_result(result: float | Decimal, precision: int = 9) -> str:
    """
    Format numerical result with intelligent precision.

    Args:
        result: Numerical result to format
        precision: Significant figures for output formatting

    Returns:
        String representation with appropriate precision
    """
    if isinstance(result, Decimal):
        if not result.is_finite():
            return str(result)
        return f"{result:.{precision}g}"

    if isinstance(result, (int, float)):
        if isinstance(result, float) and (math.isnan(result) or math.isinf(result)):
            return str(result)
        return f"{result:.{precision}g}"

    return str(result)

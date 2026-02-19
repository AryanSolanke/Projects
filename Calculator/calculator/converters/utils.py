"""
Converter Utilities

Shared helpers for converter modules.
All computations use Decimal for high accuracy - no float dependencies.
"""

from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import Optional


def to_decimal(value, value_type: str = "Value") -> Decimal:
    """
    Convert numeric values to Decimal with type checking.

    Args:
        value: Numeric value to convert (Decimal or int)
        value_type: Name of value for error messages

    Returns:
        Decimal representation
    """
    if isinstance(value, Decimal):
        return value
    # Prevent bool from passing via int subclassing.
    if isinstance(value, bool):
        raise TypeError(f"{value_type} must be numeric, got {type(value).__name__}")
    if isinstance(value, int):
        return Decimal(value)
    raise TypeError(f"{value_type} must be numeric, got {type(value).__name__}")


def get_numeric_input(prompt: str = "") -> Optional[Decimal]:
    """
    Prompt user for numeric input with error handling.

    Args:
        prompt: Input prompt message

    Returns:
        Decimal value if valid, None otherwise
    """
    try:
        raw = input(prompt).strip()
        if raw == "":
            return None
        return Decimal(raw)
    except (InvalidOperation, ValueError, TypeError):
        return None


def format_numeric_result(result, precision: int = 9) -> str:
    """
    Format numerical result with intelligent precision.

    Args:
        result: Numerical result to format
        precision: Significant figures for output formatting

    Returns:
        String representation with appropriate precision
    """
    if not isinstance(result, Decimal):
        try:
            result = Decimal(str(result))
        except (InvalidOperation, TypeError):
            return str(result)
    if not result.is_finite():
        return str(result)
    return f"{result:.{precision}g}"

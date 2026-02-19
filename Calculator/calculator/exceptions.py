"""
Custom exceptions for calculator.
"""


class CalculatorError(Exception):
    """Base exception for calculator errors."""


class ExpressionError(CalculatorError):
    """Invalid expression."""


class DivisionByZeroError(CalculatorError):
    """Division by zero attempted."""


class UnbalancedParenthesesError(CalculatorError):
    """Unbalanced parentheses in expression."""

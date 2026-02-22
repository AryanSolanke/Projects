"""
Custom exceptions for calculator.
"""


class CalculatorError(Exception):
    """Base exception for calculator errors."""

    def __init__(self, message="\nInternal error: Something went wrong.\n"):
        super().__init__(message)

class ExpressionError(CalculatorError):
    """Invalid expression."""

    def __init__(self, message="\nMath Error: Invalid expression. Please type a valid expression.\n"):
        super().__init__(message)

class InvalidInputError(CalculatorError):
    """Invalid Input"""

    def __init__(self, message="\nInput Error: Invalid Input.\n"):
        super().__init__(message)


class NullInputError(CalculatorError):
    """Empty input given."""

    def __init__(self, message="\nNo input given.\n"):
        super().__init__(message)

class UnbalancedParenthesesError(CalculatorError):
    """Unbalanced parentheses in expression."""

    def __init__(self, message="\nError: Unbalanced Parenthesis. Maybe you forgot to close a parenthesis.\n"):
        super().__init__(message)

class DomainError(CalculatorError):
    """Raised when input is outside the valid domain for a function."""

    def __init__(self, message="\nDomain Error: Given value is out of domain range.\n"):
        super().__init__(message)


class AsymptoteError(CalculatorError):
    """Raised when input approaches a function's asymptote."""

    def __init__(self, message="\nAsysmptote Error: Input approached function's asymptote.\n"):
        super().__init__(message)
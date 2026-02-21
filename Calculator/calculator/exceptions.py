"""
Custom exceptions for calculator.
"""


class CalculatorError(Exception):
    """Base exception for calculator errors."""

    def __init__(self, message="\nInternal error: Something went wrong.\n"):
        super.__init__(message)

class ExpressionError(CalculatorError):
    """Invalid expression."""

    def __init__(self, message="\nError: Invalid expression. Please type a valid expression.\n"):
        super.__init__(message)

class InvalidInputError(CalculatorError):
    """Invalid Input"""

    def __init__(self, message="\nError: Invalid Input.\n"):
        super.__init__(message)


class NullInputError(CalculatorError):
    """Empty input given."""

    def __init__(self, message="\nNo input given.\n"):
        super.__init__(message)

class UnbalancedParenthesesError(CalculatorError):
    """Unbalanced parentheses in expression."""

    def __init__(self, message="\nError: Unbalanced Parenthesis. Maybe you forgot to close a parenthesis.\n"):
        super.__init__(message)
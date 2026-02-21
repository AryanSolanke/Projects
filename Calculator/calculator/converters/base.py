"""
Base converter class.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Dict, Tuple, Optional

from calculator.config import MENU_WIDTH
from calculator.converters.converter_utils import get_numeric_input, format_numeric_result
from calculator.exceptions import NullInputError, ExpressionError, InvalidInput

class BaseConverter(ABC):
    """
    Abstract base class for unit converters.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Converter name (e.g., 'ANGLE', 'TEMPERATURE')."""

    @property
    @abstractmethod
    def emoji(self) -> str:
        """Emoji icon for this converter."""

    @property
    @abstractmethod
    def units(self) -> Dict[int, Tuple[str, str]]:
        """Mapping of unit ID to (name, abbreviation)."""

    @abstractmethod
    def convert(self, value: Decimal, from_unit: int, to_unit: int) -> Decimal:
        """Perform the conversion."""

    def display_menu(self) -> None:
        """Display converter menu with all available units."""
        print("\n" + "=" * MENU_WIDTH)
        header = f"{self.emoji}  {self.name} CONVERSION" if self.emoji else f"{self.name} CONVERSION"
        print(header)
        print("=" * MENU_WIDTH)
        for unit_id, (name, abbrev) in self.units.items():
            print(f"  {unit_id:2d}. {name} ({abbrev})")
        quit_id = max(self.units.keys()) + 1
        print(f"\n  {quit_id:2d}. Quit {self.name.title()} Converter")
        print("=" * MENU_WIDTH)

    def get_value_prompt(self, unit_name: str) -> str:
        """Prompt shown for entering the value."""
        return f"\nEnter {unit_name.lower()}: "

    def format_result(self, result: Decimal) -> str:
        """Format the conversion result."""
        return format_numeric_result(result)

    def run(self) -> None:
        """Main conversion interface."""
        try:
            self.display_menu()

            from_unit = int(input("\nEnter FROM unit: "))
            quit_id = max(self.units.keys()) + 1
            if from_unit == quit_id:
                return
            if from_unit not in self.units:
                raise InvalidInput(f"Invalid choice. Please select 1-{max(self.units.keys())}.")

            to_unit = int(input("Enter TO unit: "))
            if to_unit == quit_id:
                return
            if to_unit not in self.units:
                raise InvalidInput(f"Invalid choice. Please select 1-{max(self.units.keys())}.")
        
            if from_unit == to_unit:
                print("\nInput and output units are the same. No conversion needed.\n")
                return

            unit_name = self.units[from_unit][0]
            value = get_numeric_input(self.get_value_prompt(unit_name))
            if value is None:
                raise NullInputError()

            result = self.convert(value, from_unit, to_unit)

            from_name, from_abbrev = self.units[from_unit]
            to_name, to_abbrev = self.units[to_unit]

            print("\n" + "=" * MENU_WIDTH)
            print("   CONVERSION RESULT:")
            print(f"   {value} {from_abbrev} = {self.format_result(result)} {to_abbrev}")
            print(f"   ({from_name} -> {to_name})")
            print("=" * MENU_WIDTH + "\n")

        except ValueError:
            raise InvalidInput("Please enter a valid unit number")
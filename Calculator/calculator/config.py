"""
Central configuration for calculator.
"""

from pathlib import Path
from typing import Final

# Directories
REPO_ROOT: Final = Path(__file__).resolve().parents[1]
HISTORY_DIR: Final = REPO_ROOT / "history"
HISTORY_DIR.mkdir(exist_ok=True)

# History files
STD_HISTORY_FILE: Final = HISTORY_DIR / "standard_history.txt"
SCI_HISTORY_FILE: Final = HISTORY_DIR / "scientific_history.txt"

# Precision settings
DECIMAL_PRECISION: Final = 14
DISPLAY_PRECISION: Final = 9
INTERNAL_PRECISION: Final = 60

# UI settings
ENABLE_EMOJIS: Final = True
MENU_WIDTH: Final = 50

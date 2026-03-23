"""History management for the scientific calculator."""

from calculator.config import SCI_HISTORY_FILE

HISTORY_FILE = SCI_HISTORY_FILE


def display_hist_sci_calc(history_file=HISTORY_FILE) -> None:
    """Display scientific calculation history from file."""
    try:
        if not history_file.exists():
            print("\nNo history file found. Try performing a calculation first!")

        history = history_file.read_text(encoding="utf-8").strip()

        if not history:
            print("\nHistory is currently empty.")
        else:
            print("\n--- Scientific Calculation History ---")
            print(history)

    except (PermissionError, UnicodeDecodeError, OSError):
        print("Internal Error: Failed reading history")


def record_history_sci_calc(name: str, val, answer: str, history_file=HISTORY_FILE) -> None:
    """Append scientific calculation to history file."""
    try:
        with history_file.open("a", encoding="utf-8") as f:
            f.write(f"{name}({val}) = {answer}\n")
    except (FileNotFoundError, PermissionError, UnicodeDecodeError, OSError):
        print("Internal Error: Failed to record history")


def clear_hist_sci_calc(history_file=HISTORY_FILE) -> None:
    """Clear all scientific history by truncating the history file."""
    try:
        with history_file.open("w", encoding="utf-8"):
            print("Scientific history cleared successfully!")
    except (FileNotFoundError, PermissionError, UnicodeDecodeError, OSError):
        print("Internal Error: Failed to clear history")




"""
Programmer Calculator Module

Provides bitwise operations, bit shifts, and bidirectional base conversions
(DEC, HEX, BIN, OCT). All operations are performed using Python integers
for exact, arbitrary-precision integer arithmetic — no float dependencies.

Word size (BYTE/WORD/DWORD/QWORD) controls the bit-width mask applied to
results, exactly like the Windows Calculator programmer mode.
"""

from __future__ import annotations

from enum import IntEnum
from textwrap import dedent

from calculator.standard import errmsg


# ============================================================================
# Word Size Configuration
# ============================================================================

class WordSize(IntEnum):
    """Supported word sizes (bit widths)."""
    BYTE  =  8   # 8-bit unsigned
    WORD  = 16   # 16-bit unsigned
    DWORD = 32   # 32-bit unsigned
    QWORD = 64   # 64-bit unsigned


# Cycle order matching Windows Calculator: QWORD → DWORD → WORD → BYTE → QWORD
WORD_SIZE_CYCLE = [WordSize.QWORD, WordSize.DWORD, WordSize.WORD, WordSize.BYTE]
WORD_SIZE_LABELS = {
    WordSize.QWORD: "QWORD (64-bit)",
    WordSize.DWORD: "DWORD (32-bit)",
    WordSize.WORD:  "WORD  (16-bit)",
    WordSize.BYTE:  "BYTE  ( 8-bit)",
}

# Current word size (module-level state, toggled by user)
_word_size: WordSize = WordSize.QWORD


def get_word_size() -> WordSize:
    """Return the current word size."""
    return _word_size


def toggle_word_size() -> WordSize:
    """Cycle to the next word size and return it."""
    global _word_size
    idx = WORD_SIZE_CYCLE.index(_word_size)
    _word_size = WORD_SIZE_CYCLE[(idx + 1) % len(WORD_SIZE_CYCLE)]
    return _word_size


def _mask(value: int) -> int:
    """Apply the current word-size mask and interpret as a signed integer."""
    bits = int(_word_size)
    unsigned = value & ((1 << bits) - 1)
    # Convert to two's-complement signed
    if unsigned >= (1 << (bits - 1)):
        return unsigned - (1 << bits)
    return unsigned


def _unsigned_mask(value: int) -> int:
    """Apply the current word-size mask, keeping value unsigned."""
    bits = int(_word_size)
    return value & ((1 << bits) - 1)


# ============================================================================
# Base Conversion Helpers
# ============================================================================

def _parse_int(raw: str) -> int:
    """
    Parse an integer from a string, auto-detecting base:
    - Prefixes: 0x / 0X (hex), 0b / 0B (bin), 0o / 0O (oct)
    - Plain digits: decimal
    - Plain letters (A-F without prefix): treated as hex
    """
    raw = raw.strip()
    if not raw:
        raise ValueError("Empty input")
    try:
        return int(raw, 0)
    except ValueError:
        # Try as plain hex (e.g. "FF" without "0x")
        return int(raw, 16)


def dec_to_hex(n: int) -> str:
    """Convert decimal integer to uppercase hex string (no prefix)."""
    if n < 0:
        # Two's complement hex for the current word size
        bits = int(_word_size)
        n = _unsigned_mask(n)
    return hex(n)[2:].upper()


def dec_to_bin(n: int) -> str:
    """Convert decimal integer to binary string padded to word size."""
    bits = int(_word_size)
    n = _unsigned_mask(n)
    raw = bin(n)[2:]
    # Group into nibbles for readability
    padded = raw.zfill(bits)
    groups = [padded[i:i+4] for i in range(0, len(padded), 4)]
    return " ".join(groups)


def dec_to_oct(n: int) -> str:
    """Convert decimal integer to octal string (no prefix)."""
    n = _unsigned_mask(n)
    return oct(n)[2:]


def hex_to_dec(s: str) -> int:
    """Convert hex string to signed decimal integer (respects word size)."""
    return _mask(int(s.strip(), 16))


def hex_to_bin(s: str) -> str:
    """Convert hex string to binary (padded to word size)."""
    return dec_to_bin(int(s.strip(), 16))


def hex_to_oct(s: str) -> str:
    """Convert hex string to octal."""
    return dec_to_oct(int(s.strip(), 16))


def bin_to_dec(s: str) -> int:
    """Convert binary string to signed decimal integer."""
    s = s.replace(" ", "")
    return _mask(int(s, 2))


def bin_to_hex(s: str) -> str:
    """Convert binary string to hex."""
    return dec_to_hex(int(s.replace(" ", ""), 2))


def bin_to_oct(s: str) -> str:
    """Convert binary string to octal."""
    return dec_to_oct(int(s.replace(" ", ""), 2))


def oct_to_dec(s: str) -> int:
    """Convert octal string to signed decimal integer."""
    return _mask(int(s.strip(), 8))


def oct_to_hex(s: str) -> str:
    """Convert octal string to hex."""
    return dec_to_hex(int(s.strip(), 8))


def oct_to_bin(s: str) -> str:
    """Convert octal string to binary."""
    return dec_to_bin(int(s.strip(), 8))


def show_all_bases(n: int) -> str:
    """Show a number in all four bases simultaneously."""
    u = _unsigned_mask(n)
    return (
        f"  DEC : {n}\n"
        f"  HEX : {dec_to_hex(u)}\n"
        f"  BIN : {dec_to_bin(u)}\n"
        f"  OCT : {dec_to_oct(u)}"
    )


# ============================================================================
# Bitwise Operations
# ============================================================================

def bitwise_and(a: int, b: int) -> int:
    """Bitwise AND."""
    return _mask(a & b)


def bitwise_or(a: int, b: int) -> int:
    """Bitwise OR."""
    return _mask(a | b)


def bitwise_xor(a: int, b: int) -> int:
    """Bitwise XOR."""
    return _mask(a ^ b)


def bitwise_not(a: int) -> int:
    """Bitwise NOT (one's complement, word-size aware)."""
    bits = int(_word_size)
    return _mask(~a)


def bitwise_nand(a: int, b: int) -> int:
    """Bitwise NAND."""
    return bitwise_not(a & b)


def bitwise_nor(a: int, b: int) -> int:
    """Bitwise NOR."""
    return bitwise_not(a | b)


def bitwise_xnor(a: int, b: int) -> int:
    """Bitwise XNOR."""
    return bitwise_not(a ^ b)


# ============================================================================
# Bit Shift Operations
# ============================================================================

def shift_arithmetic_left(value: int, n: int) -> int:
    """
    Arithmetic shift left (ASL).
    Equivalent to multiplication by 2^n (overflow wraps within word size).
    """
    return _mask(value << n)


def shift_arithmetic_right(value: int, n: int) -> int:
    """
    Arithmetic shift right (ASR).
    Preserves the sign bit — divides by 2^n rounding toward negative infinity.
    """
    bits = int(_word_size)
    # Work in signed space
    signed = _mask(value)
    # Python's >> on negative ints already does arithmetic (sign-extending)
    return _mask(signed >> n)


def shift_logical_left(value: int, n: int) -> int:
    """
    Logical shift left (LSL).
    Same as arithmetic shift left; zeros fill from the right.
    """
    return _mask(_unsigned_mask(value) << n)


def shift_logical_right(value: int, n: int) -> int:
    """
    Logical shift right (LSR).
    Zeros fill from the left regardless of sign bit.
    """
    return _mask(_unsigned_mask(value) >> n)


def rotate_left(value: int, n: int) -> int:
    """
    Rotate left (circular shift left, ROL).
    Bits shifted out of the MSB wrap back into the LSB.
    """
    bits = int(_word_size)
    n = n % bits
    u = _unsigned_mask(value)
    rotated = ((u << n) | (u >> (bits - n))) & ((1 << bits) - 1)
    return _mask(rotated)


def rotate_right(value: int, n: int) -> int:
    """
    Rotate right (circular shift right, ROR).
    Bits shifted out of the LSB wrap back into the MSB.
    """
    bits = int(_word_size)
    n = n % bits
    u = _unsigned_mask(value)
    rotated = ((u >> n) | (u << (bits - n))) & ((1 << bits) - 1)
    return _mask(rotated)


def rotate_left_carry(value: int, n: int, carry: int) -> tuple[int, int]:
    """
    Rotate left through carry (RCL).
    The carry flag is treated as an extra bit, making it an (N+1)-bit rotation.
    Returns (result, new_carry).
    """
    bits = int(_word_size)
    carry = carry & 1
    n = n % (bits + 1)
    u = _unsigned_mask(value)
    extended = (u << 1) | carry          # bits+1 wide: value | carry at LSB
    mask_ext = (1 << (bits + 1)) - 1
    rotated_ext = (((extended << (n - 1)) | (extended >> (bits + 1 - (n - 1)))) & mask_ext) if n else extended
    # Simpler iterative for clarity / correctness:
    result_u = u
    new_carry = carry
    for _ in range(n % (bits + 1)):
        msb = (result_u >> (bits - 1)) & 1
        result_u = ((result_u << 1) | new_carry) & ((1 << bits) - 1)
        new_carry = msb
    return _mask(result_u), new_carry


def rotate_right_carry(value: int, n: int, carry: int) -> tuple[int, int]:
    """
    Rotate right through carry (RCR).
    The carry flag is treated as an extra bit.
    Returns (result, new_carry).
    """
    bits = int(_word_size)
    carry = carry & 1
    result_u = _unsigned_mask(value)
    new_carry = carry
    for _ in range(n % (bits + 1)):
        lsb = result_u & 1
        result_u = ((new_carry << (bits - 1)) | (result_u >> 1)) & ((1 << bits) - 1)
        new_carry = lsb
    return _mask(result_u), new_carry


# ============================================================================
# Input Helpers
# ============================================================================

def _get_int(prompt: str) -> int | None:
    """Prompt user for an integer in any base."""
    raw = input(prompt).strip()
    if not raw:
        return None
    try:
        return _parse_int(raw)
    except (ValueError, OverflowError):
        print("Error: Invalid integer. Use decimal, 0x hex, 0b binary, or 0o octal.")
        return None


def _get_shift_amount() -> int | None:
    """Prompt for a shift/rotate amount."""
    raw = input("Enter shift amount: ").strip()
    try:
        n = int(raw)
        if n < 0:
            print("Error: Shift amount must be non-negative.")
            return None
        return n
    except ValueError:
        print("Error: Invalid shift amount.")
        return None


# ============================================================================
# Menu Display Functions
# ============================================================================

def prog_main_menu() -> None:
    """Display the programmer calculator main menu."""
    ws_label = WORD_SIZE_LABELS[_word_size]
    print(dedent(f"""
        {'='*55}
        PROGRAMMER CALCULATOR          [{ws_label}]
        {'='*55}
        1. Base Conversion     (DEC / HEX / BIN / OCT)
        2. Bitwise Operations  (AND, OR, XOR, NOT, NAND, NOR, XNOR)
        3. Bit Shift           (Arithmetic, Logical, Rotate, Carry)
        4. Toggle Word Size    (QWORD → DWORD → WORD → BYTE)
        5. Quit Programmer Calculator
        {'='*55}"""))


def base_conv_menu() -> None:
    """Display the base-conversion sub-menu."""
    print(dedent("""
        ──────────────────────────────────────────
        BASE CONVERSION  (enter any prefix or none)
          Decimal : plain digits, e.g. 255
          Hex     : 0xFF  or  FF
          Binary  : 0b11111111
          Octal   : 0o377
        ──────────────────────────────────────────
        1.  DEC → HEX / BIN / OCT  (show all)
        2.  HEX → DEC / BIN / OCT  (show all)
        3.  BIN → DEC / HEX / OCT  (show all)
        4.  OCT → DEC / HEX / BIN  (show all)
        5.  Back
        ──────────────────────────────────────────"""))


def bitwise_menu() -> None:
    """Display the bitwise-operations sub-menu."""
    print(dedent("""
        ──────────────────────────────────────────
        BITWISE OPERATIONS
        ──────────────────────────────────────────
        1.  AND   (A & B)
        2.  OR    (A | B)
        3.  XOR   (A ^ B)
        4.  NOT   (~A)
        5.  NAND  (~(A & B))
        6.  NOR   (~(A | B))
        7.  XNOR  (~(A ^ B))
        8.  Back
        ──────────────────────────────────────────"""))


def shift_menu() -> None:
    """Display the bit-shift sub-menu."""
    print(dedent("""
        ──────────────────────────────────────────
        BIT SHIFT
        ──────────────────────────────────────────
        1.  Arithmetic Shift Left  (ASL)
        2.  Arithmetic Shift Right (ASR)
        3.  Logical Shift Left     (LSL)
        4.  Logical Shift Right    (LSR)
        5.  Rotate Left            (ROL)
        6.  Rotate Right           (ROR)
        7.  Rotate Left  + Carry   (RCL)
        8.  Rotate Right + Carry   (RCR)
        9.  Back
        ──────────────────────────────────────────"""))


# ============================================================================
# Sub-menu Handlers
# ============================================================================

def _print_result(label: str, value: int) -> None:
    """Print a result with all base representations."""
    print(f"\n  ┌─ {label}")
    print(show_all_bases(value))
    print()


def handle_base_conversion() -> None:
    """Interactive base-conversion sub-menu."""
    while True:
        base_conv_menu()
        try:
            choice = int(input("Enter choice: "))
        except (ValueError, TypeError):
            errmsg()
            continue

        if choice == 5:
            break

        if choice == 1:
            raw = input("Enter decimal value: ").strip()
            try:
                n = int(raw)
                _print_result(f"DEC {n}", n)
            except ValueError:
                errmsg()

        elif choice == 2:
            raw = input("Enter hex value (e.g. FF or 0xFF): ").strip()
            try:
                n = hex_to_dec(raw.replace("0x", "").replace("0X", ""))
                _print_result(f"HEX {raw.upper()}", n)
            except ValueError:
                errmsg()

        elif choice == 3:
            raw = input("Enter binary value (e.g. 1010 or 0b1010): ").strip()
            raw = raw.replace("0b", "").replace("0B", "").replace(" ", "")
            try:
                n = bin_to_dec(raw)
                _print_result(f"BIN {raw}", n)
            except ValueError:
                errmsg()

        elif choice == 4:
            raw = input("Enter octal value (e.g. 377 or 0o377): ").strip()
            raw = raw.replace("0o", "").replace("0O", "")
            try:
                n = oct_to_dec(raw)
                _print_result(f"OCT {raw}", n)
            except ValueError:
                errmsg()
        else:
            errmsg()


def handle_bitwise() -> None:
    """Interactive bitwise-operations sub-menu."""
    while True:
        bitwise_menu()
        try:
            choice = int(input("Enter choice: "))
        except (ValueError, TypeError):
            errmsg()
            continue

        if choice == 8:
            break

        if choice == 4:
            # Unary NOT
            a = _get_int("Enter value A: ")
            if a is None:
                continue
            result = bitwise_not(a)
            _print_result(f"NOT {a}", result)
            continue

        if choice not in range(1, 8):
            errmsg()
            continue

        a = _get_int("Enter value A: ")
        if a is None:
            continue
        b = _get_int("Enter value B: ")
        if b is None:
            continue

        ops = {
            1: ("AND",  bitwise_and),
            2: ("OR",   bitwise_or),
            3: ("XOR",  bitwise_xor),
            5: ("NAND", bitwise_nand),
            6: ("NOR",  bitwise_nor),
            7: ("XNOR", bitwise_xnor),
        }
        label_str, op_func = ops[choice]
        result = op_func(a, b)
        _print_result(f"{a} {label_str} {b}", result)


def handle_bit_shift() -> None:
    """Interactive bit-shift sub-menu."""
    while True:
        shift_menu()
        try:
            choice = int(input("Enter choice: "))
        except (ValueError, TypeError):
            errmsg()
            continue

        if choice == 9:
            break

        if choice not in range(1, 9):
            errmsg()
            continue

        value = _get_int("Enter value: ")
        if value is None:
            continue
        n = _get_shift_amount()
        if n is None:
            continue

        if choice in (7, 8):
            # Rotate through carry — need a carry input
            try:
                carry_raw = int(input("Enter carry flag (0 or 1): ").strip())
                carry = carry_raw & 1
            except (ValueError, TypeError):
                print("Error: Carry must be 0 or 1.")
                continue

            if choice == 7:
                result, new_carry = rotate_left_carry(value, n, carry)
                print(f"\n  ROL carry: value={value}, n={n}, carry_in={carry}")
                print(f"  carry_out = {new_carry}")
            else:
                result, new_carry = rotate_right_carry(value, n, carry)
                print(f"\n  ROR carry: value={value}, n={n}, carry_in={carry}")
                print(f"  carry_out = {new_carry}")
            _print_result("Result", result)
            continue

        shift_ops = {
            1: ("ASL", shift_arithmetic_left),
            2: ("ASR", shift_arithmetic_right),
            3: ("LSL", shift_logical_left),
            4: ("LSR", shift_logical_right),
            5: ("ROL", rotate_left),
            6: ("ROR", rotate_right),
        }
        label_str, shift_func = shift_ops[choice]
        result = shift_func(value, n)
        _print_result(f"{value} {label_str} {n}", result)


# ============================================================================
# Main Programmer Calculator Entry Point
# ============================================================================

def programmer_calc() -> None:
    """Main programmer calculator interface."""
    while True:
        prog_main_menu()
        try:
            choice = int(input("Enter choice: "))
        except (ValueError, TypeError, KeyboardInterrupt):
            errmsg()
            continue

        if choice == 1:
            handle_base_conversion()
        elif choice == 2:
            handle_bitwise()
        elif choice == 3:
            handle_bit_shift()
        elif choice == 4:
            new_ws = toggle_word_size()
            print(f"\n  Word size set to: {WORD_SIZE_LABELS[new_ws]}\n")
        elif choice == 5:
            print("\n  Programmer calculator closed!\n")
            break
        else:
            errmsg()

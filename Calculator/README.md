# 🧮 Advanced Modular Calculator

A robust, enterprise-grade console-based Python calculator featuring modular architecture, comprehensive unit conversions, and extensive mathematical functions. Built with clean code principles, domain-driven design, and test-driven development.

## 🌟 Features Overview

### 📊 Standard Calculator
- **Expression Evaluation**: Evaluates complex arithmetic expressions with full operator precedence
- **Persistent History**: All calculations are saved with file-based storage
- **Error Resilience**: Gracefully handles division by zero, syntax errors, and malformed input
- **Smart Formatting**: Removes trailing zeros and floating-point artifacts

### 🔬 Scientific Calculator
- **24 Engineering Functions**: Complete suite of trigonometric, inverse trigonometric, hyperbolic, and inverse hyperbolic functions
- **Domain Validation**: Explicit mathematical domain checks prevent undefined results
- **High Precision**: Results formatted to 9 significant figures with intelligent rounding
- **O(1) Dispatch**: Dictionary-based function lookup using tuple-key mapping for optimal performance

### 🔄 Unit Converter
Comprehensive conversion system supporting **5 categories**:

#### 📐 Angle Conversion
- Degrees, Radians, Gradians
- Bidirectional conversions

#### 🌡️ Temperature Conversion  
- Celsius, Kelvin, Fahrenheit
- Full bidirectional support

#### ⚖️ Weight Conversion
- **13 Units**: Kilogram, Gram, Milligram, Centigram, Decigram, Decagram, Hectogram, Metric Tonne, Ounce, Pound, Stone, Short Ton (US), Long Ton (UK)
- **182 Conversion Pairs**: Universal converter handles all unit combinations
- Metric and Imperial systems

#### 💨 Pressure Conversion
- **6 Units**: Atmosphere, Bar, Kilopascal, mmHg, Pascal, PSI
- **30 Conversion Pairs**: Medical, meteorological, and engineering standards
- Commonly used in weather, diving, automotive, and industrial applications

#### 💾 Data Conversion
- **35 Units**: Bits, Bytes, Nibbles, KB/KiB, MB/MiB, GB/GiB, TB/TiB, PB/PiB, EB/EiB, ZB/ZiB, YB/YiB
- **1,190 Conversion Pairs**: Covers both decimal (SI) and binary (IEC) standards
- Understand the difference between GB (1000³) and GiB (1024³)
- Perfect for computer science, networking, and data storage calculations

## 🎯 Key Technical Highlights

### Architecture
- **Modular Design**: Clear separation of concerns (std, sci, converter package)
- **Package Structure**: Organized converter submodules with clean imports
- **Zero Dependencies**: Pure Python implementation (except testing)

### Mathematical Correctness
- **Domain Guarding**: Every function validates input domains
  - `sin⁻¹(x)` → valid only for -1 ≤ x ≤ 1
  - `sec(x)` → undefined at 90° + n·180°
  - `coth(x)` → undefined at x = 0
- **Precision Handling**: Deterministic formatting with no floating-point junk
- **Error Messages**: Clear, human-readable feedback instead of crashes

### Performance
- **O(1) Function Dispatch**: Tuple-key dictionary mapping eliminates long if-else chains
- **Universal Converters**: Single function handles all unit pairs efficiently
- **Minimal Overhead**: Direct mathematical operations with no unnecessary abstraction

### Code Quality
- **Type Hints**: Full type annotations throughout codebase
- **Docstrings**: Comprehensive documentation for all public functions
- **Consistent Style**: PEP 8 compliant with standardized formatting
- **Error Handling**: Defensive programming with graceful degradation

## 📁 Project Structure

```
Calculator/
│
├── main.py                      # Application entry point & UI orchestration
├── std.py                       # Standard arithmetic engine
├── sci.py                       # Scientific functions engine
├── converters.py               # Unit converter router
│
├── converter/                   # Converter package (5 modules)
│   ├── __init__.py             # Package initialization
│   ├── angle_converter.py      # Angle conversions
│   ├── temp_converter.py       # Temperature conversions
│   ├── weight_converter.py     # Weight conversions
│   ├── pressure_converter.py   # Pressure conversions
│   └── data_converter.py       # Data unit conversions (35 units)
│
└── tests/                      # Comprehensive test suite
    ├── test_std.py            # Standard calculator tests (68 tests)
    ├── test_sci.py            # Scientific calculator tests (87 tests)
    └── test_converter.py     # Converter tests (237 tests)
```

## 🚀 Installation & Usage

### Prerequisites
- Python 3.8 or higher
- No external dependencies for running the calculator
- pytest required for running tests (optional)

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YourUsername/Calculator.git
   cd Calculator
   ```

2. **Run the calculator**:
   ```bash
   python main.py
   ```

3. **Run tests** (optional):
   ```bash
   pytest tests/ -v
   ```

### Usage Examples

#### Standard Calculator
```
➤ Enter expression (e.g., 2+3*4): (2 + 3) * 5 / (7 - 2)
✅ Result: 5
```

#### Scientific Calculator
```
➤ Enter operation number: 1
➤ Enter sub-operation number: 1
📐 Enter angle in degrees: 30
✅ Result: sin(30°) = 0.5
```

#### Unit Converter - Data Conversion
```
💾 DATA UNIT CONVERSION
➤ Enter FROM unit (1-35): 24
➤ Enter TO unit (1-35): 25
💾 Enter data amount: 500

✅ CONVERSION RESULT:
   500.0 GB = 465.66 GiB
   (Gigabyte → Gibibyte)
```

## 🧪 Testing

The project includes 392 comprehensive tests covering:
- ✅ Normal operations and edge cases
- ✅ Domain violations and error handling
- ✅ Boundary values and extreme inputs
- ✅ Round-trip conversion accuracy
- ✅ Symmetry and mathematical properties

### Test Coverage
- **Standard Calculator**: Expression evaluation, history management, error handling
- **Scientific Calculator**: All 24 functions across all quadrants, domain validation
- **Converters**: Accuracy verification, bidirectional consistency, unit validation

### Running Tests
```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_std.py -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

## 🔧 Technical Details

### Converter Capabilities

#### Data Converter - Understanding SI vs IEC Standards

**Why does my 500 GB hard drive show only 465 GB?**

- **Hard Drive Label**: 500 GB (Decimal/SI)
  - Uses base 1000: 500,000,000,000 bytes
  
- **Operating System**: Shows 465.66 GiB (Binary/IEC)
  - Uses base 1024: 500,000,000,000 ÷ 1,073,741,824 = 465.66 GiB

**No space is missing - just different measurement systems!**

The data converter handles:
- **Decimal units (SI)**: KB, MB, GB, TB, PB, EB, ZB, YB (powers of 1000)
- **Binary units (IEC)**: KiB, MiB, GiB, TiB, PiB, EiB, ZiB, YiB (powers of 1024)

## 🎓 Learning Outcomes

This project demonstrates:
- ✅ Clean modular software architecture
- ✅ Defensive programming for mathematical systems
- ✅ Domain-driven design principles
- ✅ Test-driven development methodology
- ✅ Package organization and import management
- ✅ User experience design with clear feedback
- ✅ Performance optimization through algorithmic design

## 🛠️ Technology Stack

- **Language**: Python 3.8+
- **Standard Library**: math, pathlib, enum, typing
- **Testing**: pytest framework
- **Architecture**: Modular, function-dispatch based
- **Code Style**: PEP 8 compliant

## 📋 Recent Updates

### Version 2.1 - Integrated Data Converter (Current)
- ✅ **Data Converter Integration**: Moved data_converter.py into converter package
- ✅ **5 Converter Categories**: Angle, Temperature, Weight, Pressure, Data
- ✅ **Enhanced Menu System**: Updated converter router for data conversions
- ✅ **1,190 Data Conversions**: Complete SI and IEC standard support
- ✅ **Consistent Package Structure**: All converters in unified package

### Version 2.0 - Major Refactor
- ✅ **Modular Converter Architecture**: Separated converters into independent modules
- ✅ **Enhanced User Interface**: Added emojis and improved formatting for better UX
- ✅ **Standardized Documentation**: Consistent docstrings and comments across all modules
- ✅ **Import System Overhaul**: Resolved all import conflicts with proper package structure
- ✅ **Expanded Unit Support**: Added pressure conversions (6 units, 30 conversion pairs)
- ✅ **Code Quality**: Standardized commenting style, improved error messages
- ✅ **Test Coverage**: All 392 tests passing with comprehensive edge case coverage

## 📝 Code Quality Standards

### Docstring Format
```python
def function_name(param: type) -> return_type:
    """
    Brief description of function purpose.
    
    Detailed explanation of behavior and any important notes.
    
    Args:
        param: Description of parameter
        
    Returns:
        Description of return value
        
    Raises:
        ErrorType: When this error occurs
    """
```

### Error Handling Pattern
```python
try:
    # Main operation
    result = operation()
except SpecificError:
    # Handle specific error
    errmsg()
except Exception:
    # Fallback handler
    errmsg()
```

## 🤝 Contributing

Contributions are welcome! Please ensure:
1. All tests pass before submitting PR
2. New features include corresponding tests
3. Code follows PEP 8 style guide
4. Docstrings are provided for all functions
5. No external dependencies added without discussion

## 📄 License

This project is available for educational and personal use.

## 🙏 Acknowledgments

Built with rigorous attention to mathematical correctness, code quality, and user experience. This project serves as a comprehensive example of professional Python development practices.

---

**Built with precision, tested with rigor, designed with care.** 🎯

**Total Conversion Capabilities**: 1,440 unique conversions across 5 categories!

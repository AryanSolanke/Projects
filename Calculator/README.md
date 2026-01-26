# 🔢 Advanced Modular Calculator

A robust, console-based Python calculator designed with a clean modular architecture that separates standard arithmetic evaluation from advanced scientific computation. This project emphasizes mathematical correctness, domain safety, and test-driven reliability, making it far more than a basic calculator.

## 🚀 Key Highlights
* **Modular and scalable design (std vs sci separation)**
* **Strict mathematical domain validation (no silent math errors)**
* **Deterministic numeric formatting (no floating-point junk or ignored decimals)**
* **O(1) function dispatch using tuple-key dictionary mapping**
* **Extensively tested using pytest across edge cases, limits, and invalid inputs**

## 🛠️ Standard Mode
### Expression Evaluation
* **Evaluates arithmetic expressions like:**'(2 + 3) * 5 / (7 - 2)'.
* **Supports nested parentheses and operator precedence.**
### Error Resilience
* **Gracefully handles:**
   * **Division by zero**
   * **Invalid syntax**
   * **Runtime evaluation errors**
* **Application never crashes on malformed input.**

## 🧪 Scientific Mode
* **24 Engineering Functions**: Includes full suites for Trigonometric, Inverse Trigonometric, Hyperbolic, and Inverse Hyperbolic functions.
* **High Efficiency**: Uses $O(1)$ dictionary lookups with tuple-key mapping for function execution.

## 🧠 Domain Guarding (Critical Feature)
Every function is protected by explicit mathematical domain checks, preventing undefined or misleading results.
Examples:
* **sin⁻¹(x) → valid only for -1 ≤ x ≤ 1**
* **sec(x) → invalid at 90° + n·180°**
* **coth(x) → undefined at x = 0**
Instead of crashing, the calculator returns clear, human-readable error messages.

## 🎯 Precision Handling
* **Results are formatted to high precision**
* **Trailing zeros and floating-point artifacts are removed**
* **-0 is normalized to 0**
This ensures:
cos(0.0001) = 1
not 0.9999999999998**

## ⚡ Performance Design
* **Function execution uses O(1) dictionary lookup via tuple-key mapping**
* **No long if–else chains**
* **Clean separation of UI logic and computation engine**

## 🧪 Testing & Reliability
### This project includes a large pytest test suite covering:
* **Normal, inverse, and hyperbolic functions**
* **Domain violations**
* **Division-by-zero cases**
* **Very large and very small inputs**
* **Symmetry and sign correctness**
* **Invalid and non-numeric inputs**
Testing ensures mathematical correctness and stability across all supported operations.

## 📁 Project Structure
Calculator/
│
├── main.py # Entry point & menu-driven UI
├── std.py # Standard arithmetic engine & error handling
├── sci.py # Scientific math logic, validation & formatting
├── tests/
│ ├── test_std.py
│ └── test_sci.py
└── README.md

## 🛠️ Tech Stack
* **Language: Python 3.13**
* **Math Engine: math module**
* **Architecture: Modular, function-dispatch based**
* **Testing: pytest**

## 📥 Installation & Usage
1. **Clone the repository**:
   git clone [https://github.com/AryanSolanke/Calculator.git](https://github.com/AryanSolanke/Calculator.git)
2. **Navigate to the Repository**:
   cd (path)\Calculator\
3. **Run the application**:
  python main.py

## 🧠 Learning Outcomes
### This project demonstrates:
* **Clean modular software design**
* **Defensive programming for mathematical systems**
* **Precision-aware numerical computation**
* **Test-driven development for scientific code**

## ⭐ Milestone Note
This version marks a major architectural and mathematical milestone, featuring a full refactor of the scientific engine and the introduction of exhaustive automated testing.
If you’re reviewing the commit history, this is the point where the project transitions from a simple calculator to a reliable computation system.

📌 Built with rigor, not shortcuts.
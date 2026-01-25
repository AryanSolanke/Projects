# 🔢 Advanced Modular Calculator 

A robust, console-based Python application that separates standard arithmetic from complex scientific computations. This project demonstrates modular programming, efficient data structures (tuple-key mapping), and rigorous mathematical domain validation.

## 🚀 Key Features

### 🛠️ Standard Mode
* **Expression Parsing**: Uses a flexible evaluation engine to process strings like `(2+3)*5`.
* **Error Resilience**: Handles division by zero and syntax errors without crashing.

### 🧪 Scientific Mode
* **24 Engineering Functions**: Includes full suites for Trigonometric, Inverse Trigonometric, Hyperbolic, and Inverse Hyperbolic functions.
* **Domain Guarding**: Custom validation layer prevents `Math Domain Errors` by checking inputs against mathematical boundaries (e.g., ensuring $|x| \le 1$ for $\sin^{-1}(x)$).
* **High Efficiency**: Uses $O(1)$ dictionary lookups with tuple-key mapping for function execution.

## 📁 Project Structure
* `main.py` — Entry point & Tree-structured UI logic.
* `std.py` — Arithmetic engine & global error handlers.
* `sci.py` — Scientific math functions & domain validation.

## 🛠️ Tech Stack
* **Language**: Python 3.13
* **Core Logic**: Math module, Dictionary Mapping, Recursion-based UI.

## 📥 Installation & Usage
1. **Clone the repository**:
   git clone [https://github.com/AryanSolanke/Calculator.git](https://github.com/AryanSolanke/Calculator.git)
2. **Navigate to the Repository**
3. **Run the application**:
  python main.py
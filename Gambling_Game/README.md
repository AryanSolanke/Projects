# Gambling Game

Simple command-line jackpot game written in Python — a beginner-friendly project for practicing input handling, control flow and basic functions.

**Files**
- `Gambling_game.py`: Main program (play the jackpot game).

**Requirements**
- Python 3.8+ (recommended).
- No external packages required — uses only the standard library.

**Run**
1. Open a terminal in the project folder.
2. Run:

```bash
python Gambling_game.py
```

**How to play**
- The program starts with a main menu; choose the jackpot game to begin.
- You start with an initial balance (set in the script).
- For each round:
	- Enter the amount you want to gamble (max $500 per round).
	- Guess a jackpot number between 0 and 5.
	- If your guess matches the random jackpot number, your wager is doubled.

**Notes & tips**
- Input is validated; enter integers when prompted.
- Press Ctrl+C (or send EOF) to exit gracefully.
- You can change rules (max gamble, jackpot range) by editing the constants at the top of `Gambling_game.py`.

**Project goals / learning outcomes**
- Practice writing CLI programs and handling user input.
- Learn to separate logic into small functions for clarity.

**Disclaimer**
This project is for learning purposes only. No real money is involved.

**Author**
- Aryan Solanke — GitHub: https://github.com/AryanSolanke

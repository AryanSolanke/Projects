import random
import textwrap

#global variables
MAX_GAMBLE=500
JACKPOT_MIN=0
JACKPOT_MAX=5

def get_choice(msg):
    while True:
        try:
            return int(input(msg))
        except ValueError:
            print("Invalid input, please enter an integer")

def print_Jackno_rules():
        print(textwrap.dedent("""
            ++==++jackpot number game guide++==++\n
            Rule: Max $500/gamble per round.
            How to Play:
            1. Enter a number in given range (0-5),
            2. Enter amount to be gambled,
            3. If the number you entered is the jackpot number your invested amount is doubled,
            4. Continue playing or exit the game.\n"""))


def validate_gambleno(gambleno):
    return JACKPOT_MIN<=gambleno<=JACKPOT_MAX

def validate_gambleamt(gambleamt, balance):
    return  0<gambleamt<=balance and gambleamt<=MAX_GAMBLE


def update_bal(balance, gambleamt, gambleres):
    balance -= gambleamt
    if gambleres:
        balance += gambleamt*2
    return balance

#Gambling logic
def play_round(balance, gambleamt, gambleno):
    jackno = random.randint(JACKPOT_MIN, JACKPOT_MAX)

    gambleres = (jackno==gambleno)
    balance = update_bal(balance, gambleamt, gambleres)
    return balance, gambleres

def play_jackpot(balance):
    while True:
            gambleamt = get_choice("\nEnter amount of money you want to gamble: ")
            if not validate_gambleamt(gambleamt, balance):
                print("Insufficient balance or invalid gamble amount(Check rules)")
                print(f"Current balance = {balance}")
                continue
            break
        

    while True:
            gambleno = get_choice("Guess the jackpot number: ")
            if not validate_gambleno(gambleno):
                print(f"Invalid guess, choose {JACKPOT_MIN}-{JACKPOT_MAX}")
                continue
            break

    balance, gambleres = play_round(balance, gambleamt, gambleno)

    if gambleres:
        print("Congratulations you won the jackpot!!")
        print(f"Your gambled ${gambleamt} is doubled!!")
    else:
        print(f"Oops, No luck!\nYou lost ${gambleamt} :(")
    return balance

def main():
#User inputs
    balance = 3000
    name = str(input("Enter your name: "))
    print(f"Welcome to gambling games, {name}.")
    while True:
        print("""\n|====->Menu<-====|\n1. Jackpot number gambling.\n2. Exit""", end="\n")
        game_ch= get_choice("Enter your choice: ")
    #Game choice
        match game_ch:
            case 1:
                print("\nInitial account balance = $3000")
                print_Jackno_rules()
                while True:
                    print("|====->Menu<-====|\n1.Start\n2. Quit")
                    base_choice = get_choice("Enter your choice: ")
                    match base_choice:
                        case 1:
                            balance = play_jackpot(balance)
                            print(f"New balance = {balance}")
                        case 2:
                            print("\nBye have a nice day! :D") 
                            break
                        case _:
                            print("Please enter a valid integer. Choose 1-2")
            case 2:
                print("Hoping to see you again ^-^")
                break
            case _:
                print("Invalid choice, Choose 1-2")
                continue

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")


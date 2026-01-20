import math

def summation(numbers_to_add):
    return sum(numbers_to_add)
    
def difference(numbers_to_subtract):
    diff = numbers_to_subtract[0]
    for i in numbers_to_subtract[1:]:
        diff -= i
    return diff

def div(numerator, denominator):
    return numerator / denominator

def abs_value(num):
    return abs(num)

def nth_power(base, exponent):
    return base ** exponent

def remainder(numerator, denominator):
    return numerator % denominator

def log(num):
    return math.log10(num)

def ln(num):
    return math.log(num)

def get_numbers():
    user_input = input("Enter numbers: ")
    return [float(num) for num in user_input.replace(',', ' ').split()]

print("""Select an operation:
1) Add
2) subtraction
3) Division
4) mod
5) nth Power
6) Remainder
7) Logarithm""")

while True:

    try:
        operation_num = int(input("Enter your choice: "))
        
        if operation_num < 1 or operation_num > 7:
            print("Error: Please select a valid operation number between 1 and 7.")
        else:
            break 
    except ValueError:
        print("Error: Invalid input. Please enter a number between 1 and 7.")

match operation_num:
    case 1:      
        print(f'Sum is: {summation(get_numbers())}')

    case 2:
        print(f'Difference (first minus rest): {difference(get_numbers())}')

    case 3:
        try:
            num = float(input("Enter numerator: "))
            denom = float(input("Enter denominator: "))
            if denom==0:
                print("Zero_Division_Error: Denominator can't be zero.")
            else:
                print(f'Division result: {div(num, denom)}')    
        except ValueError:
            print("Error: Invalid input.")

    case 4:
        try:
            number = float(input("Enter a number: "))
            print(f'Absolute value is: {abs_value(number)}')
        except ValueError:
            print("Error: Invalid input.")

    case 5:
        try:
            base = float(input("Enter the base: "))
            exponent = float(input("Enter the exponent: "))
            print(f'Result of {base} raised to the power of {exponent} is: {nth_power(base, exponent)}')
        except ValueError:
            print("Error: Invalid input.")

    case 6:
        try:
            numerator = float(input("Enter the numerator: "))
            denominator = float(input("Enter the denominator: "))
            print(f'Remainder is: {remainder(numerator, denominator)}')
        except ValueError or ZeroDivisionError:
            print("Error: Inavlid input. You can't enter string or denomenator as 0.")

    case 7:
        try:
            print("1. Natural log.\n2. Log.")
            choice = int(input("Enter your choice: "))
            if choice==1:
                num = float(input("Enter number: "))
                print(f"Ln({num}) = {ln(num)}")
            elif choice==2:
                num = float(input("Enter number: "))
                print(f"Log({num}) = {log(num)}")
            else:
                print("Error: Invalid input.")
        except ValueError:
            print("Error: Invalid input.")

    case _:
        print("Error: Please select a valid operation 1-7.")
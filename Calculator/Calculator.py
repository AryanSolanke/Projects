def summation(numbers_to_add):
    return sum(numbers_to_add)
    

def difference(numbers_to_subtract):
    diff = numbers_to_subtract[0]
    for i in numbers_to_subtract[1:]:
        diff -= i
    return diff


def div(numerator, denominator):
    try:
        return numerator / denominator
    except ZeroDivisionError:
        return "Error: Cannot divide by zero."


def abs_value(num):
    return abs(num)


def nth_power(base, exponent):
    return base ** exponent


def remainder(numerator, denominator):
    try:
        return numerator % denominator
    except ZeroDivisionError:
        return "Error: Cannot divide by zero."


def get_numbers():
    user_input = input("Enter numbers separated by commas or spaces: ")
    return [float(num) for num in user_input.replace(',', ' ').split()]


print("""Select an operation:
1) Sum
2) Sub
3) Division
4) mod
5) nth Power
6) Remainder
Enter the operation number: """)

while True:
    try:
        operation_num = int(input("Enter your chloice: "))
        
        if operation_num < 1 or operation_num > 6:
            print("Error: Please select a valid operation number between 1 and 6.")
        else:
            break 
    except ValueError:
        print("Error: Invalid input. Please enter a number between 1 and 6.")


if operation_num == 1:      
    print(f'Sum is: {summation(get_numbers())}')

elif operation_num == 2:
    print(f'Difference (first minus rest): {difference(get_numbers())}')

elif operation_num == 3:
    num = float(input("Enter numerator: "))
    denom = float(input("Enter denominator: "))
    print(f'Division result: {div(num, denom)}')

elif operation_num == 4:
    number = float(input("Enter a number: "))
    print(f'Absolute value is: {abs_value(number)}')

elif operation_num == 5:
    base = float(input("Enter the base: "))
    exponent = float(input("Enter the exponent: "))
    print(f'Result of {base} raised to the power of {exponent} is: {nth_power(base, exponent)}')

elif operation_num == 6:
    numerator = float(input("Enter the numerator: "))
    denominator = float(input("Enter the denominator: "))
    print(f'Remainder is: {remainder(numerator, denominator)}')

else:
    print("Error: Please select a valid operation number between 1 and 6.")
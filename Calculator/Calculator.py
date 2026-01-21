import math

def errmsg():
    print("Error: Invalid input.")

def menuMsg():
    print("""Select an operation:\n1) Add\n2) subtraction\n3) Division\n4) mod\n5) nth Power\n6) Remainder\n7) Logarithm\n8) Close Calc""")
    
def difference(numbers_to_subtract):
    diff = numbers_to_subtract[0]
    for i in numbers_to_subtract[1:]:
        diff -= i
    return diff

def get_numbers():
    try:
        user_input = float(input("Enter numbers: "))
        return [float(num) for num in user_input.replace(',', ' ').split()]
    except ValueError:
        errmsg()

if __name__ == "__main__":
    menuMsg()
    while True:
        try:
            operation_num = int(input("Enter your choice: "))
            
            if operation_num < 1 or operation_num > 8:
                errmsg()
            else:
                break 
        except ValueError:
            errmsg()

        match operation_num:
            case 1:      
                print(f'Sum is: {sum(get_numbers())}')
            case 2:
                print(f'Difference (first minus rest): {difference(get_numbers())}')
            case 3:
                try:
                    num = float(input("Enter numerator: "))
                    denom = float(input("Enter denominator: "))
                    if denom==0:
                        print("Zero_Division_Error: Denominator can't be zero.")
                    else:
                        print(f'Division result: {float(num/denom)}')    
                except ValueError:
                    errmsg()
            case 4:
                try:
                    number = float(input("Enter a number: "))
                    print(f'Absolute value is: {abs(number)}')
                except ValueError:
                    errmsg()
            case 5:
                try:
                    base = float(input("Enter the base: "))
                    exponent = float(input("Enter the exponent: "))
                    print(f'Result of {base} raised to the power of {exponent} is: {pow(base, exponent)}')
                except ValueError:
                    errmsg()
            case 6:
                try:
                    numerator = float(input("Enter the numerator: "))
                    denominator = float(input("Enter the denominator: "))
                    print(f'Remainder is: {numerator % denominator}')
                except ValueError or ZeroDivisionError:
                    errmsg()
            case 7:
                try:
                    print("1. Natural log.\n2. Log.")
                    choice = int(input("Enter your choice: "))
                    if choice==1:
                        num = float(input("Enter number: "))
                        print(f"Ln({num}) = {math.log10(num)}")
                    elif choice==2:
                        num = float(input("Enter number: "))
                        print(f"Log({num}) = {math.log(num)}")
                    else:
                        errmsg()
                except ValueError:
                    errmsg()
            case 8:
                print("Exiting Calc...")
                break
            case _:
                errmsg()
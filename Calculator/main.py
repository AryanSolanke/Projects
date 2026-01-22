from std_sci import *

def mode_choice_menu():
    print("\n======>Main Menu<======\n\n1. Standard\n2. Scientific\n3. Quit")

def std_calc_main_menu():
    while True:
        std_calc_menuMsg()
        try:
            op_num = int(input("Enter operation number: "))
            if not op_num:
                errmsg()
        except (ValueError, KeyboardInterrupt, UnboundLocalError):
            errmsg()
            continue
        match op_num:
            case 1:
                nums = get_numbers()
                if nums != None:
                    print(f'Sum is: {sum(nums)}')
                else:
                    errmsg()
            case 2:
                nums = get_numbers()
                if nums != None:
                    print(f'Difference (first minus rest): {difference(get_numbers())}')
                else:
                    errmsg()
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
                        print(f"Ln({num}) = {math.log(num)}")
                    elif choice==2:
                        num = float(input("Enter number: "))
                        print(f"Log({num}) = {math.log10(num)}")
                    else:
                        errmsg()
                except ValueError:
                    errmsg()
            case 8:
                try:
                    num = int(input("Enter number: "))
                    print(f"Factorial of {num} = {math.factorial(num)}")
                except ValueError:
                    errmsg()
            case 9:
                print("\nStandard calculator closed!")
                break
            case _:
                errmsg()

def sci_calc_main_menu():

    while True:
        sci_calc_menuMsg()
        try:
            op_num = int(input("Enter operation number: "))
            if not op_num:
                errmsg()
        except (ValueError, KeyboardInterrupt, UnboundLocalError):
            errmsg()
            continue
        match op_num:
            case 1:
                angle = get_angle()
                print(f"\nsin({angle}) = {math.sin(math.radians(angle))}")
            case 2:
                angle = get_angle()
                print(f"\ncos({angle}) = {math.cos(math.radians(angle))}")
            case 3:
                angle = get_angle()
                print(f"\ntan({angle}) = {math.tan(math.radians(angle))}")
            case 4: 
                angle = get_angle()
                print(f"\ncot({angle}) = {1/(math.tan(math.radians(angle)))}")
            case 5:
                angle = get_angle()
                print(f"\nsec({angle}) = {1/(math.cos(math.radians(angle)))}")
            case 6:
                angle = get_angle()
                print(f"\ncosec({angle}) = {1/(math.sin(math.radians(angle)))}")
            case 7:
                print("\nScientific calculator closed!")
                break
            case _:
                errmsg()

if __name__ == '__main__':

    try:
        while True:
            mode_choice_menu()
            try:
                mode_choice = int(input("Select a mode for Calc: "))
            except ValueError:
                errmsg()
            match mode_choice:
                case 1:
                    std_calc_main_menu()
                case 2:
                    sci_calc_main_menu()
                case 3:
                    print("\nThank you for using Calculator!")
                    break
                case _:
                    errmsg()
    except(KeyboardInterrupt, EOFError):
            print("\nProgram interrupted by user. Thank you for using Calculator!")
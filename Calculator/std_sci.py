import math

def errmsg():
    print("Error: Invalid input.")

def std_calc_menuMsg():
    print("\nSelect an operation:\n1) Add\n2) subtraction\n3) Division\n4) mod\n5) nth Power\n6) Remainder\n7) Logarithm\n8) Factorial\n9) Exit")

def sci_calc_menuMsg():
    print("\n|=====>Operations<=====|\n\n1. Sin(x)\n2. Cos(x)\n3. Tan(x)\n4. Cot(x)\n5. Sec(x)\n6. Cosec(x)\n7. Exit|======================|")
    
def difference(numbers_to_subtract):
    diff = numbers_to_subtract[0]
    for i in numbers_to_subtract[1:]:
        diff -= i
    return diff

def get_numbers():
    try:
        user_input = input("Enter numbers: ").strip()
        if not user_input:
            return []
        return [float(num) for num in user_input.split(' ')]
    except ValueError:
        errmsg()
        return None
    
def get_angle():
    try:
        num = float(input("Enter angle(degrees): "))
        return num
    except ValueError:
        errmsg()

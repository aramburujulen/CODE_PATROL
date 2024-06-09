# Code snippet 2
def calculate_rectangle_area(length, width):
    return length * width

def calculate_rectangle_perimeter(length, width):
    return 2 * (length + width)

def print_rectangle_info(length, width):
    area = calculate_rectangle_area(length, width)
    perimeter = calculate_rectangle_perimeter(length, width)
    print(f"Length: {length}")
    print(f"Width: {width}")
    print(f"Area: {area}")
    print(f"Perimeter: {perimeter}")

length = float(input("Enter the length of the rectangle: "))
width = float(input("Enter the width of the rectangle: "))
print_rectangle_info(length, width)

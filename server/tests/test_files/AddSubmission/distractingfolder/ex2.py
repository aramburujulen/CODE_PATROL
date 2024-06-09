# Code snippet 1
def calculate_area(radius):
    return 3.14 * radius ** 2

def calculate_circumference(radius):
    return 2 * 3.14 * radius

def print_circle_info(radius):
    area = calculate_area(radius)
    circumference = calculate_circumference(radius)
    print(f"Radius: {radius}")
    print(f"Area: {area}")
    print(f"Circumference: {circumference}")

radius = float(input("Enter the radius of the circle: "))
print_circle_info(radius)
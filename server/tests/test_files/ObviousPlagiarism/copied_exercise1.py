def calculate_area(radius):
    return 3.14159 * radius ** 2

def calculate_circumference(radius):
    return 2 * 3.14159 * radius

def main():
    radius = float(input("Enter the radius of the circle: "))
    area = calculate_area(radius)
    circumference = calculate_circumference(radius)
    print("Area of the circle:", area)
    print("Circumference of the circle:", circumference)

if __name__ == "__main__":
    main()
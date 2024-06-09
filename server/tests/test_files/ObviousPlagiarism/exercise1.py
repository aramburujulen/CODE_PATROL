def calculate_area(length, breadth):
    return length * breadth

def calculate_perimeter(length, breadth):
    return 2 * (length + breadth)

def main():
    length = float(input("Enter the length of the rectangle: "))
    breadth = float(input("Enter the breadth of the rectangle: "))
    area = calculate_area(length, breadth)
    perimeter = calculate_perimeter(length, breadth)
    print("Area of the rectangle:", area)
    print("Perimeter of the rectangle:", perimeter)

if __name__ == "__main__":
    main()
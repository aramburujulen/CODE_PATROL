with open('example.txt', 'w') as file:
    file.write('Hello, World!\n')
    file.write('This is a text file.\n')

# Open the file for reading
with open('example.txt', 'r') as file:
    for line in file:
        print(line.strip()) 
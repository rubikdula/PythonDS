file_path = "example.txt"
# file = open(file_path, "r")
#
# content = file.read()
# print(content)
#
# with open(file_path, "r") as file:
#     content = file.read()
#     print(content)
#
# r = Read only mode
# w = write
# a = append
# b =  Binary mode
# x = Exclusive Creation
#
# with open(file_path, "r") as file:
#     lines = file.readlines()
#     print(lines)

# with open(file_path, "w") as file:
#     file.write("Hello World!")
#
# lines = ['Hello World\n', 'Welcome to Python\n']
# with open(file_path, "w") as file:
#     file.writelines(lines)
# with open(file_path, "a") as file:
#     file.write("New data appended")
#
# data = b"this is a data"
# with open('example.bin', 'wb') as file:
#     file.write(data)
#
# with open('example.bin', 'rb') as f:
#     data = f.read()

# with open(file_path) as f:
#     for line in f:
#         clean_line = line.strip()
#         print(clean_line)
#
# with open("example.txt") as f:
#     for line in f:
#         words = line.strip().split()
#         print(words)

name = "Rubik"
age= 30

# with open("example.txt", 'w') as f:
#     f.write("Name" + name + "\nAge" + str(age))

with open("example.txt", 'w') as file:
    file.write(f"Name: {name}\n")
    file.write(f"Age: {age}")
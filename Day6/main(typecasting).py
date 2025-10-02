x = 5
y = 4

result = x + y
print(result, "of type", type(result))

a = 6
b = 7
result = a * int(b)
print(result, "of type", type(result))

print(bool(0))
print(bool(1))

print(bool(''))
print(bool("Hello"))

print(bool([]))

name = input("What is your name? ")
print(f"Hello {name}")

age = input("What is your age? ")
print(type(age))

number = int(input("What is your number? "))
number2 = int(input("What is your second number? "))

result = number + number2

print(f"The sum of {number} and {number2} is {result}")
print(type(number))
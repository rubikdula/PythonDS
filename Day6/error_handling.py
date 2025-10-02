try:
    result = 10 / 0
except ZeroDivisionError:
    print("Division by zero")

fruits = {
    "apple": 10,
    "banana": 20,
    "orange": 30,
}

try:
    print(fruits["cherry"])
except KeyError:
    print("KeyError")

text = "this is a text"
try:
    text_to_int = int(text)
except Exception as e:
    print("An error with typecasting", e)

def divide_numbers(a, b):
    try:
        result = a / b
        print("Result is: ", result)
    except ZeroDivisionError:
        print("Division by zero")
    except TypeError:
        print("TypeError")
    except Exception as e:
        print("An error with typecasting", e)

divide_numbers(2, 3)
divide_numbers(2, 3)
divide_numbers(2, "3")
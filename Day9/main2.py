def add(x, y):
    return x + y

def concatenate(x, y):
    return str(x) + str(y)

def operate(operation, x, y):


    """""
    :param this is a operation that needs to be performed:
    :param x the first operation:
    :param y the second operation:
    :return The result of the operation:
    """""
    return operation(x, y)

result_sum = operate(add, 1, 2)
result_concatenate = operate(concatenate, 2, 3)
print("The result of sum: " + str(result_sum))
print("The result of concatenate: " + str(result_concatenate))
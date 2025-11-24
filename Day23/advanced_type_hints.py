from typing import Optional
from typing import Union
from typing import Any
from typing import List

def get_name(name: Optional[str] = None) -> str:
    if name:
        return f"Hello, {name}!"
    return "Hello, Guest!"

print(get_name())

def process_value(value: Union[int, str]) -> str:
    if isinstance(value, int):
        return f"Number: {value}"
    elif isinstance(value, str):
        return f"String: {value}"
    return "Unsupported type"

print(process_value("Digital School"))

#any type
def process_anything(value: Any) -> str:
    return f"Processed value: {value}"

print(process_anything("Hello, Guest!"))

#list type
def sum_numbers(numbers: List[int]) -> int:
    return sum(numbers)

numbers = List[int] = [1, 2, 3, 4, 5]
print(f"Sum of numbers: {sum_numbers(numbers)}")
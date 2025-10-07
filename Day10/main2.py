from abc import ABC, abstractmethod

# class Student(ABC):
#     pass

# class Shape(ABC):
#     @abstractmethod
#     def area(self):
#         pass

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass
class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * self.radius * self.radius

class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side * self.side

circle1 = Circle(5)
square1 = Square(5)
print(circle1.area())
print(square1.area())


import math

class Shape:
    def area(self):
        pass

class Circle(Shape):
    def __init__ (self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius * self.radius

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

class Triangle(Shape):
    def __init__(self, base, height):
        self.base = base
        self.height = height
    def area(self):
        return self.base * self.height / 2

circle = Circle(2)
rectangle = Rectangle(4, 5)
triangle = Triangle(4, 5)

print(circle.area())
print(rectangle.area())
print(triangle.area())

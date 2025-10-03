# # # # def calculate_area(length, width):
# # # #     return length * width
# # # #
# # # # def calculate_perimeter(length, width):
# # # #     return 2 * (length + width)
# # # #
# # # # length = 5
# # # # perimeter = 3
# # # #
# # # # area = calculate_area(length, perimeter)
# # # # perimeter = calculate_perimeter(length, perimeter)
# # #
# # # # class rectangle:
# # # #     def __init__(self, length, width):
# # # #         self.length = length
# # # #         self.width = width
# # # #
# # # #     def calculate_area(self):
# # # #         return self.length * self.width
# # # #
# # # #     def calculate_perimeter(self):
# # # #         return 2 * (self.length + self.width)
# # # #
# # # # my_rectangle = rectangle(5, 5)
# # # # area = my_rectangle.calculate_area()
# # # # perimeter = my_rectangle.calculate_perimeter()
# # # # print("Area:", area)
# # # # print("Perimeter:", perimeter)
# # #
# # # # class Person:
# # # #     def __init__(self, name, age):
# # # #         self.name = name
# # # #         self.age = age
# # # #
# # # #     def greet(self):
# # # #         return f"Hello, my name is {self.name} and I am {self.age} years old."
# # # #
# # # # person1 = Person("Alice", 30)
# # # # person2 = Person("Bob", 20)
# # # # print(person1.greet())
# # # # print(person2.greet())
# # #
# # # class Student:
# # #     school_name = "ABC High School"
# # #
# # # student1 = Student()
# # #
# # # print(student1.school_name)
# # #
# #
# # class Student:
# #     school_name = "ABC High School"
# #
# #     def __init__(self, name, age):
# #         self.name = name
# #         self.age = age
# #         self.course = course
# #
# # student1 = Student("Rion", 20, "Math")
# # student2 = Student("Alice", 22, "Science")
# #
# # print(student1.course)
# # print(student2.course)
#
# class myClass:
#     def __init__(self):
#         self.__private_variable = "This is a private variable"
#         self.public_variable = "This is a public variable"
#
#     def __private_method(self):
#         return "This is a private method"
#
# my_class = myClass()
# print(my_class.public_variable)
# my_class.__private_method()
# print(my_class.__private_variable)

class MyClass:
    def __init__(self):
        self._protected_variable = "This is a protected variable"

        def get_protected_method(self):
            return self._protected_variable

my_class = MyClass()
print(my_class._protected_variable)

my_class._protected_method()
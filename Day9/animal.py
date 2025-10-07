class Animal:
    def __init__(self, name):
        self.name = name

    def sound(self):
        print("Some generic animal sound")
    def description(self):
        return f"This is an animal named {self.name}."
#
# class Dog(Animal):
#     def __init__(self, name, breed):
#         super().__init__(name)
#         self.breed = breed
#
#     def sound(self):
#         print("Dog sound")
#
#     def description(self):
#         super().description()
#         return f"This is a {self.breed} dog named {self.name}."

class Cat(Animal):
    def __init__(self, name, color):
        super().__init__(name)
        self.color = color

    def sound(self):
        print("Cat sound")

    def description(self):
        super().description()
        return f"This is a {self.color} cat named {self.name}."

dog = Dog("Buddy", "Golden Retriever")
cat = Cat("Whiskers", "White")
dog.description()
cat.description()
dog.sound()
cat.sound()
animal = Animal("Generic Animal")
animal.sound()
print(animal.description())

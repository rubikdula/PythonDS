# Key OOP Principles: Encapsulation, Inheritance, Polymorphism, Abstraction

# class superClass:
#     class Subclass(superClass):

class Animal:
    def sound(self):
        print("Some generic animal sound")

# class Dog(Animal):
#     def bark(self):
#         print("Woof! Woof!")
#     def eat(self):
#         print("The dog is eating dog food.")

class Cat(Animal):
    def sound(self):
        print("Meow! Meow!")

class Dog(Animal):
    def sound(self):
        print("Woof! Woof!")

animal = Animal()
animal.sound()

cat = Cat()
cat.sound()
dog = Dog()
dog.sound()
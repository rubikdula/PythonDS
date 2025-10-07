class Dog:
    def __init__(self, name):
        self.name = name

    def sound(self):
        print(f"{self.name} says hello")

class Cat:
    def __init__(self, name):
        self.name = name

    def sound(self):
        print(f"{self.name} says hi")

class Bird:
    def __init__(self, name):
        self.name = name
    def sound(self):
        print(f"{self.name} says Pershendetje")

dog = Dog("Dog")
cat = Cat("Cat")
bird = Bird("Bird")

for animal in [dog, cat, bird]:
    animal.sound()
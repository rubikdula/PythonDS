class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age


@property
def name(self):
    return self.__name

@name.setter
def name(self, name):
    self.__name = name

@property
def age(self):
    return self.__age

@age.setter
def age(self, age):
    self.__age = age

s = Student("John", 36)
print(s.name)
print(s.age)

s.name = "Ylli"
s.age = 56

print("Updated name of Student is: ", s.name)
print("Updated age of Student is: ", s.age)
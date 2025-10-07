class Student:
    def __init__(self,name,age):
        self.__name=name
        self.__age=age

    def get_name(self):
        return self.__name
    def set_name(self,name):
        self.__name=name
    def get_age(self):
        return self.__age
    def set_age(self,age):
        self.__age=age

student=Student("John",36)
student.set_name("Pork")
print("Updated name is: " , student.get_name())
student.get_age()
student.set_age(36)
print("Updated age is: ", student.get_age())

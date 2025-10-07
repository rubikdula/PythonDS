from abc import ABC, abstractmethod

class DigitalSchool(ABC):
    def __init__(self, City, State, Courses):
        self.City = City
        self.State = State
        self.Courses = Courses

    @property
    def City(self):
        return self.__City

    @City.setter
    def City(self, City):
        self.__City = City

    @property
    def State(self):
        return self.__State

    @State.setter
    def State(self, State):
        self.__State = State

    @property
    def Courses(self):
        return self.__Courses

    @State.setter
    def Courses(self, Courses):
        self.__Courses = Courses

    def show_school_info(self):
        print(f"City: {self.City}")
        print(f"State: {self.State}")
        print(f"Courses: {self.Courses}")

    @abstractmethod
    def organize_hackathon(self):
        pass


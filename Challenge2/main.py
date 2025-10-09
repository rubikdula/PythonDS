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

    @Courses.setter
    def Courses(self, Courses):
        self.__Courses = Courses

    def show_school_info(self):
        print(f"City: {self.City}")
        print(f"State: {self.State}")
        print(f"Courses: {self.Courses}")

    @abstractmethod
    def organize_hackathon(self):
        pass


class DS_Prishtina(DigitalSchool):
    def __init__(self, City, State, Courses, student_number):
        super().__init__(City, State, Courses)
        self.student_number = student_number

    @property
    def student_number(self):
        return self.__student_number

    @student_number.setter
    def student_number(self, student_number):
        self.__student_number = student_number

    def SCF(self):
        print("Spring Code Fest (SCF) – DS Prishtina")
        print("Tracks: AI, Web, Cybersecurity")

    def organize_hackathon(self):
        print("DS Prishtina Hackathon is happening!")
        print(f"Location: {self.City}, {self.State}")
        print("Duration: 24 hours, Team size: 3–5")


ds = DS_Prishtina("Prishtina", "Kosovo", "Python, Web, Cybersecurity", 250)

ds.SCF()
ds.organize_hackathon()

print()
ds.show_school_info()
print()
print(f"The number of DS_Prishtina is {ds.student_number}")

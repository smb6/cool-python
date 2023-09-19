# Python program to demonstrate
# use of class method and static method.
from datetime import date


class Person:
    version = 0.1

    def __init__(self, name, age):
        self.middle_name = None
        self.name = name
        self.age = age

    # a class method to create a Person object by birth year.
    @classmethod
    def fromBirthYear(cls, name, year):
        return cls(name, date.today().year - year)

    # a static method to check if a Person is adult or not.
    @staticmethod
    def isAdult(age):
        return age > 18

    def middle_name(self, name):
        self.middle_name = name
        return self.middle_name

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, var: int):
        self.version = var


if __name__ == "__main__":

    person1 = Person('mayank', 21)
    person2 = Person.fromBirthYear('mayank', 1996)

    print(person1.age)
    print(person2.age)

    print(person1.version)
    person1.version = 2
    print(person1.version)
    print(person2.version)
    # print the result
    print(Person.isAdult(22))



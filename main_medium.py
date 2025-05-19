
class Parent:
    def greet(self):
        print("Parent")

class Child(Parent):
    def greet(self):
        super().greet()
        print("Child")


obj = Child()
obj.greet()

class A:
    def show(self):
        print("A")

class B(A):
    def show(self):
        print("B")
        super().show()

class C(A):
    def show(self):
        print("C")
        super().show()

class D(B, C):
    def show(self):
        print("D")
        super().show()

from dataclasses import dataclass

@dataclass
class Person:
    name: str
    age: int



if __name__ == "__main__":
    obj = D()
    obj.show()

    """
    https://medium.com/pythoneers/stop-writing-python-code-like-its-2009-modernize-your-projects-today-18e1b7be960e
    """
    p = Person("Jon", 25)
    print(f"{p.name=}")
    print(f"{p.age=}")

    from collections import Counter
    numbers = [1, 2, 2, 3, 3, 3]
    count_dict = Counter(numbers)
    print(count_dict)

    from pathlib import Path
    file_path = Path("directory") / "file.txt"
    if file_path.exists():
        content = file_path.read_text()
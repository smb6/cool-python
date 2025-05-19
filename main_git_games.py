
def git_func():
    print("First commit")
    print("Second commit")
    print("Third commit, is this correct?")
    print("Fourth commit")

from dataclasses import dataclass

@dataclass
class Person:
    name: str
    age: int


if __name__ == "__main__":
    words = ["apple", "banana", "apple"]
    word_count = {}
    for word in words:
        word_count[word] = word_count.get(word, 0) + 1
    from collections import Counter
    c = Counter(word_count)
    git_func()
    p = Person("Jon", 25)
    print(f"{p.name=}")
    print(f"{p.age=}")

    from collections import Counter

    numbers = [1, 2, 2, 3, 3, 3]
    count_dict = Counter(numbers)
    print(count_dict)

    # def modify_number(num):
    #     num += 10
    #     return num
    #
    #
    # x = 5
    # modify_number(x)
    #
    # print(x)
    #
    # import os
    # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # print(__file__)
    # print(BASE_DIR)

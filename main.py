# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import sys
import pathlib
from functools import cached_property

PYTHON_VERSION = float(sys.version_info[0]) + float(sys.version_info[1] / 10)


def print_hi(name):
    basic = BasicStuff()
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.
    print(f'Python version is {basic.python_version}')

    name = "Mike"
    surname = "Doe"
    print(f"{name=}, {surname=}")

    first_dictionary = dict(name="Mike", occupation="Python Developer")
    second_dictionary = dict(location="Iowa", hobby="Surf")
    # In python 3.9 use the following
    if basic.python_version >= 3.9:
        merged_dictionary = first_dictionary | second_dictionary
    else:
        merged_dictionary = {**first_dictionary, **second_dictionary}

    print(merged_dictionary)

    file_path = "xxx"
    path = pathlib.Path(file_path)
    path.touch()
    if path.exists():
        print(f"What {file_path} is?\nfile? {path.is_file()}\ndir? {path.is_dir()}")
        path.unlink(missing_ok=False)
    else:
        print(f"File {file_path} doesn't exist")

    # Merge 2 even list into a dict
    list1 = [1, 2, 3]
    list2 = ['one', 'two', 'three']
    new_dictionary = dict(zip(list1, list2))
    print(f"Creating new dictionary from: {list1=} and {list2=}:\n{new_dictionary}")

    # Merge 2 uneven list into a dict
    from itertools import cycle
    list1 = ['A', 'B', 'C', 'D', 'E']
    list2 = ['1', '2', '3']
    print(f"Uneven lists with no special handling {dict(zip(list1, list2))}")
    new_dictionary = dict(zip(list1, cycle(list2)))
    print(f"Uneven lists with cycle special handling {new_dictionary}")


class BasicStuff:

    @cached_property
    def mac_address(self) -> str:
        from uuid import getnode
        # Strip off hex character from front
        _mac = hex(getnode())[2:]
        # Add semicolons every two characters
        mac = ":".join([_mac[i:i + 2] for i in range(0, len(_mac), 2)])
        return mac

    @cached_property
    def python_version(self) -> float:
        version = float(sys.version_info[0]) + float(sys.version_info[1] / 10)
        return version


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    basic = BasicStuff()
    print(basic.mac_address)
    print(type(basic.python_version))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

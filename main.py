# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import copy
import sys
import json
import pathlib
import logging
from functools import cached_property
from opensky_api import OpenSkyApi

from datetime import datetime

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
    logging.info(f"Creating new dictionary from: {list1=} and {list2=}:\n{new_dictionary}")

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
        _mac = hex(getnode())[2:]  # Strip off hex character from front
        # Add semicolons every two characters
        mac = ":".join([_mac[i:i + 2] for i in range(0, len(_mac), 2)])
        return mac

    @cached_property
    def python_version(self) -> float:
        version = float(sys.version_info[0]) + float(sys.version_info[1] / 10)
        return version


def flights_info(bbox: tuple = None, min_height: int = 1000):
    # min_height = 1000
    api = OpenSkyApi()
    s = api.get_states(bbox=bbox)
    flights_low = [x for x in s.states if x.geo_altitude is not None and x.geo_altitude < min_height]
    for f in flights_low:
        print(f)


def _list_of_dicts_keys():
    _list_of_dicts = [
        {"name": "Tom", "age": 10},
        {"name": "Mark", "age": 5, "height": 4},
        {"name": "Pam", "age": 7, "Zone": 3}
    ]
    all_keys = set().union(*(d.keys() for d in _list_of_dicts))
    all_keys_sorted_i = sorted(all_keys, key=str.casefold)
    print(all_keys_sorted_i)


def _to_json():
    sample = {"name": "Pam", "age": 7, "Zone": 3}
    sample['title'] = "String"
    sample['somedate'] = datetime.utcnow()
    _jsoned = json.dumps(sample, sort_keys=True, default=str)
    print(_jsoned)
    exit(99)


def _dict_join():
    # Initializing the dictionaries
    d1 = {'fruit': 'Apple', 'calories': 100}
    d2 = {'vegetable': 'Tomato', 'calories': 50}
    print("d1: ", d1)
    print("d2: ", d2)
    # Using lambda function first copies d1 in l, it will then update l by merging it with d2
    merge = (lambda l=d1.copy(): (l.update(d2), l)[1])()
    m = d1.copy()
    n = (m.update(d2), m)
    print("Resultant merged Dictionary: ", merge)
    exit(99)


def get_mac_address() -> hex:
    from uuid import getnode
    mac = hex(getnode())
    return mac


def func_cool_in_staging(name: str):
    print(f"Hello {name}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(get_mac_address())
    _dict_join()
    _to_json()
    _list_of_dicts_keys()
    ascii = [chr(n) for n in range(256)]  # No errors
    print(ascii)  # No errors
    print(dict(zip(ascii, ascii)))  # No errors
    import csv

    ascii_0 = copy.deepcopy(ascii)
    ascii_0.pop(0)
    data_0 = csv.DictReader(ascii_0)
    for line in data_0:
        print(line)  # No Errors

    data = csv.DictReader(ascii)
    for line in data:
        print(line)  # NULL Byte Error
    # logging.basicConfig(filename="sample.log", filemode="w", level=logging.INFO,
    #                     format='%(asctime)s - %(funcName)s - %(levelname)s: %(message)s')
    # print_hi('PyCharm')
    # basic = BasicStuff()
    # print(basic.mac_address)
    # logging.info(f"The mac address is {basic.mac_address}")
    # logging.error("THIS IS AN ERROR LOG MESSAGE")
    # print(type(basic.python_version))
    #
    # languages = ['Java', 'C++', 'Rust', 'Python', 'Julia', 'Javascript']
    # f, *_, l = languages
    # lang = copy.deepcopy(languages)
    # for l in languages:
    #     languages.remove(l)
    # print(languages)
    #
    # https://opensky-network.org/api/states/all?lamin=31.20497889719949&lomin=34.95291492180309&lamax=32.17278392864499&lomax=35.90107084724819
    # [min_latitude, max_latitude, min_longitude, max_latitude]
    # KS area
    bbox = (32.20497889719949, 32.17278392864499, 34.95291492180309, 3.90107084724819)
    # Hasharon area
    # 32.27777909571126, 34.83415550030797
    # 32.020708710245614, 34.99773932311293
    bbox = (32.020708710245614, 32.27777909571126, 34.83415550030797, 34.99773932311293)
    a = flights_info(bbox=bbox, min_height=1000)
    print(a)
    func_cool_in_staging("CShell")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

# SELECT SUBSTRING(
#                   Code,CHARINDEX('/',Code)+1,
#                   (
#                   LEN(Code-CHARINDEX('#', REVERSE(Code)
#                   )
#                   )-
#                   CHARINDEX('/',Code)
#                   )
#                   ) AS Result FROM #tb

# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import copy
import sys
import pathlib
import logging
from functools import cached_property
from opensky_api import OpenSkyApi
from typing import List


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
        _mac = hex(getnode())[2:]       # Strip off hex character from front
        # Add semicolons every two characters
        mac = ":".join([_mac[i:i + 2] for i in range(0, len(_mac), 2)])
        return mac

    @cached_property
    def python_version(self) -> float:
        version = float(sys.version_info[0]) + float(sys.version_info[1] / 10)
        return version

def flights_info(bbox: tuple = None, min_height: int = 10000) -> List:
    # min_height = 1000
    api = OpenSkyApi()
    s = api.get_states(bbox=bbox)
    flights_low = [x for x in s.states if x.geo_altitude is not None and x.geo_altitude < min_height]
    for f in flights_low:
        print(f"{f.callsign=}, {f.origin_country=}, {f.geo_altitude=}, {f.latitude=}, {f.longitude=}, {f.vertical_rate}")
    return flights_low


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
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
    a = flights_info(bbox=bbox, min_height=3000)
    print(a)


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

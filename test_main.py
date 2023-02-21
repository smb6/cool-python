import pytest
import re
import logging
import sys
import inspect

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# handler = logging.StreamHandler(sys.stdout)
# handler.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# logger.addHandler(handler)


# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# file_handler = logging.FileHandler(filename='tmp.log')
# stdout_handler = logging.StreamHandler(stream=sys.stdout)
# handlers = [file_handler, stdout_handler]
#
# logging.basicConfig(
#     level=logging.DEBUG,
#     format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
#     handlers=handlers
# )
#
# logger = logging.getLogger(__name__)


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('tmp.log')
sh = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('[%(asctime)s] %(levelname)s [%(filename)s.%(funcName)s:%(lineno)d] %(message)s',
                              datefmt='%a, %d %b %Y %H:%M:%S')
fh.setFormatter(formatter)
sh.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(sh)


def extract_ctry_date_and_ext_from_filename(filename: str):
    file_name_regex_pat = r"(\w+)_(\d{8})\.(.*)"

    if matches := re.match(file_name_regex_pat, filename):
        return matches.groups()
    else:
        raise ValueError(f"{filename} is not a valid filename")


# parametrize with fixture
@pytest.fixture(scope="session")
def start_session():
    func_name_inspect = inspect.currentframe().f_code.co_name
    func_name_sys = sys._getframe().f_code.co_name
    logger.info("\n" + "*" * 50 + "\n")
    yield
    logger.info("\n\n" + "#" * 50)


@pytest.fixture(scope="session")
def setup_chip():
    func_name_inspect = inspect.currentframe().f_code.co_name
    func_name_sys = sys._getframe().f_code.co_name
    logger.info(f"{func_name_inspect} - SETUP")
    yield
    logger.info(f"{func_name_inspect} - TEARDOWN")


@pytest.fixture(scope="session")
def firmware_setup():
    func_name_inspect = inspect.currentframe().f_code.co_name
    logger.info(f"{func_name_inspect} - SETUP")
    yield
    logger.info(f"{func_name_inspect} - TEARDOWN")


@pytest.fixture(scope="class")
def software_setup():
    func_name_inspect = inspect.currentframe().f_code.co_name
    logger.info(f"{func_name_inspect} - SETUP")
    yield
    logger.info(f"{func_name_inspect} - TEARDOWN")


@pytest.fixture(scope="module")
def test_us_csv_file_name():
    return "us_20220917.csv"


@pytest.fixture(scope="module")
def test_gb_csv_file_name():
    return "gb_20220917.csv"


@pytest.mark.usefixtures("start_session", "setup_chip", "firmware_setup", "software_setup")
@pytest.mark.parametrize(
    "filename,expected",
    [
        # 1. pass fixture name as a string
        ("test_us_csv_file_name", ("us", "20220917", "csv")),
        ("test_gb_csv_file_name", ("gb", "20220917", "csv")),
    ],
)
def test_extract_ctry_date_and_ext_from_fileanme(filename, expected, request):
    # 2. add 'request' fixture to the test's arguments ^^

    # 3. convert string to fixture value
    filename = request.getfixturevalue(filename)
    assert extract_ctry_date_and_ext_from_filename(filename) == expected

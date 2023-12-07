import re
from collections import OrderedDict


def parse_enum(ts_enum):
    # Regular expression to extract enum name and values
    enum_match = re.search(r'enum\s+(\w+)\s*\{([^}]+)\}', ts_enum)

    if enum_match:
        enum_name = enum_match.group(1)
        # enum_values_match = re.findall(r'(\w+)', enum_match.group(2))
        enum_values_match = enum_match.group(2).split(",")
        enum_values = [value.strip() for value in enum_values_match]
        enums = OrderedDict()
        for n in enum_values:
            if n:
                val = n.split("=")
                if len(val) > 1:
                    enums[val[0].strip()] = val[1].strip()
                else:
                    enums[val[0].strip()] = None

        return enum_name, enums
    else:
        return None


def generate_python_enum(enum_name, enum_values):
    # Generating Python enum class code
    python_enum_class = f"class {enum_name}(Enum):\n"

    for key, value in enum_values.items():
        if value:
            python_enum_class += f"    {key} = {value}\n"
        else:
            python_enum_class += f"    {key} = auto()\n"

    return python_enum_class


def main(input_file, output_file):
    with open(input_file, 'r') as file:
        ts_enums = file.read()

    # Splitting TypeScript enums in the file
    ts_enums_list = re.split(r'(?<=}\s)', ts_enums)

    write_once = True
    for ts_enum in ts_enums_list:
        enum_info = parse_enum(ts_enum)
        if enum_info:
            enum_name, enum_values = enum_info
            python_enum_code = generate_python_enum(enum_name, enum_values)

            # Writing Python enum code to output file
            with open(output_file, 'a') as output:
                if write_once:
                    output.write("from enum import Enum, auto\n\n\n")
                    write_once = False
                output.write(python_enum_code)
                output.write('\n\n')


if __name__ == "__main__":
    input_file = "/Users/pablo/work/git/cool-python/tmp/enums.ts"  # Replace with your TypeScript enum file
    output_file = "/Users/pablo/work/git/cool-python/tmp/output.py"  # Replace with the desired output Python file

    # main(input_file, output_file)

    import re

    text = "Some text id: 12345 file: 4424a4-35arr-aarr33 More text"

    # Define a regular expression pattern
    pattern = r'id:\s*(\S+)\s*file:\s*(\S+)'

    # Search for the pattern in the text
    match = re.search(pattern, text)

    if match:
        # Extract the text captured by the regex group
        extracted_id = match.group(1)
        extracted_file = match.group(2)
        print(f"{extracted_id=} - {extracted_file=}")
    else:
        print("Pattern 'id:' not found in the text.")
